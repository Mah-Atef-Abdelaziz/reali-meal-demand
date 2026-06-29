"""Chatbot Service — LangChain-powered conversational AI with RAG."""
import os
import sys
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
from models import PredictionResult, MealTransaction, WorkLocation, Department, Employee


class ChatbotService:
    """NLP chatbot using OpenAI (or Ollama fallback) with database tools."""

    def __init__(self):
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        """Initialize LLM — OpenAI primary, Ollama fallback."""
        try:
            if settings.use_openai:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model=settings.OPENAI_MODEL,
                    api_key=settings.OPENAI_API_KEY,
                    temperature=0.3, max_tokens=1000
                )
            else:
                from langchain_community.llms import Ollama
                self.llm = Ollama(
                    base_url=settings.OLLAMA_BASE_URL,
                    model=settings.OLLAMA_MODEL,
                    temperature=0.3
                )
        except Exception as e:
            print(f"LLM init warning: {e}")
            self.llm = None

    async def generate_response(self, message: str, session_id: str,
                                 db: AsyncSession) -> tuple:
        """Generate a response to the user's message."""
        # Gather context data from database
        context = await self._gather_context(message, db)

        if self.llm:
            return await self._llm_response(message, context)
        else:
            return self._rule_based_response(message, context)

    async def _gather_context(self, message: str, db: AsyncSession) -> dict:
        """Query database for relevant context based on the question."""
        context = {}
        msg_lower = message.lower()
        today = date.today()
        tomorrow = today + timedelta(days=1)

        # Prediction data
        if any(w in msg_lower for w in ["predict", "tomorrow", "expect", "forecast", "how many"]):
            result = await db.execute(
                select(PredictionResult)
                .where(PredictionResult.prediction_date == tomorrow)
            )
            preds = result.scalars().all()
            if preds:
                context["predictions"] = {
                    "date": str(tomorrow),
                    "breakfast": sum(p.predicted_count for p in preds if p.period == "breakfast"),
                    "lunch": sum(p.predicted_count for p in preds if p.period == "lunch"),
                    "dinner": sum(p.predicted_count for p in preds if p.period == "dinner"),
                    "total": sum(p.predicted_count for p in preds),
                    "avg_confidence": round(sum(float(p.confidence_score or 0.85) for p in preds) / max(len(preds), 1), 2),
                }

        # Waste data
        if any(w in msg_lower for w in ["waste", "wasted", "reduce", "save"]):
            week_ago = today - timedelta(days=7)
            result = await db.execute(
                select(
                    func.count(MealTransaction.id).label("total"),
                ).where(MealTransaction.transaction_date >= week_ago,
                        MealTransaction.was_wasted == True)
            )
            waste_count = result.scalar() or 0
            total_result = await db.execute(
                select(func.count(MealTransaction.id))
                .where(MealTransaction.transaction_date >= week_ago)
            )
            total_meals = total_result.scalar() or 1
            context["waste"] = {
                "period": "last 7 days",
                "wasted_meals": waste_count,
                "total_meals": total_meals,
                "waste_rate": round(waste_count / total_meals * 100, 1),
            }

        # Location data
        if any(w in msg_lower for w in ["location", "site", "where", "highest", "which"]):
            result = await db.execute(
                select(WorkLocation.name, WorkLocation.location_type,
                       func.count(MealTransaction.id).label("meals"))
                .join(MealTransaction, MealTransaction.location_id == WorkLocation.id)
                .where(MealTransaction.transaction_date >= today - timedelta(days=7))
                .group_by(WorkLocation.name, WorkLocation.location_type)
                .order_by(text("meals DESC")).limit(5)
            )
            context["top_locations"] = [{"name": r.name, "type": r.location_type,
                                          "meals_7d": r.meals} for r in result.all()]

        # Department data
        if any(w in msg_lower for w in ["department", "dept", "most", "consume"]):
            result = await db.execute(
                select(Department.name, func.count(MealTransaction.id).label("meals"))
                .join(Employee, Employee.id == MealTransaction.employee_id)
                .join(Department, Department.id == Employee.department_id)
                .where(MealTransaction.transaction_date >= today - timedelta(days=30))
                .group_by(Department.name)
                .order_by(text("meals DESC")).limit(5)
            )
            context["top_departments"] = [{"name": r.name, "meals_30d": r.meals}
                                           for r in result.all()]

        # Accuracy data
        if any(w in msg_lower for w in ["accuracy", "accurate", "performance"]):
            result = await db.execute(
                select(PredictionResult)
                .where(PredictionResult.prediction_date >= today - timedelta(days=7),
                       PredictionResult.actual_count.isnot(None))
            )
            preds = result.scalars().all()
            if preds:
                import numpy as np
                actuals = [p.actual_count for p in preds]
                predicted = [p.predicted_count for p in preds]
                mae = np.mean(np.abs(np.array(actuals) - np.array(predicted)))
                context["accuracy"] = {"period": "last 7 days", "mae": round(float(mae), 1),
                                        "samples": len(preds)}

        # Employee count
        emp_result = await db.execute(
            select(func.count(Employee.id)).where(Employee.is_active == True)
        )
        context["active_employees"] = emp_result.scalar() or 0

        return context

    async def _llm_response(self, message: str, context: dict) -> tuple:
        """Generate response using LLM."""
        system_prompt = """You are REAL.i AI Assistant, a smart meal demand prediction assistant for a food service company.
You help kitchen managers and operations staff understand meal demand predictions, food waste, and operational metrics.
Be concise, professional, and data-driven. Use the provided context data to answer questions accurately.
If data is not available, say so honestly. Format numbers with commas for readability.
Always end with a helpful follow-up suggestion."""

        context_str = f"\n\nCurrent Data Context:\n{self._format_context(context)}"
        full_prompt = f"{system_prompt}{context_str}\n\nUser Question: {message}"

        try:
            response = self.llm.invoke(full_prompt)
            text = response.content if hasattr(response, 'content') else str(response)
            return text, context
        except Exception as e:
            return self._rule_based_response(message, context)

    def _rule_based_response(self, message: str, context: dict) -> tuple:
        """Fallback rule-based response when LLM is unavailable."""
        msg_lower = message.lower()

        if "predictions" in context and any(w in msg_lower for w in ["predict", "tomorrow", "how many", "expect"]):
            p = context["predictions"]
            text = (f"📊 **Tomorrow's Meal Predictions ({p['date']})**\n\n"
                    f"🌅 Breakfast: **{p['breakfast']:,}** meals\n"
                    f"☀️ Lunch: **{p['lunch']:,}** meals\n"
                    f"🌙 Dinner: **{p['dinner']:,}** meals\n"
                    f"📈 Total: **{p['total']:,}** meals\n"
                    f"🎯 Confidence: **{p['avg_confidence']:.0%}**")
            return text, context

        if "waste" in context and any(w in msg_lower for w in ["waste", "reduce"]):
            w = context["waste"]
            text = (f"♻️ **Food Waste Report ({w['period']})**\n\n"
                    f"Wasted meals: **{w['wasted_meals']:,}** out of {w['total_meals']:,}\n"
                    f"Waste rate: **{w['waste_rate']}%**\n\n"
                    f"💡 By using AI predictions, we can reduce waste by an estimated 40-60%.")
            return text, context

        if "top_locations" in context:
            locs = context["top_locations"]
            text = "📍 **Top Locations by Demand (Last 7 Days)**\n\n"
            for i, l in enumerate(locs, 1):
                text += f"{i}. {l['name']} ({l['type']}): **{l['meals_7d']:,}** meals\n"
            return text, context

        if "top_departments" in context:
            depts = context["top_departments"]
            text = "🏢 **Top Departments by Consumption (Last 30 Days)**\n\n"
            for i, d in enumerate(depts, 1):
                text += f"{i}. {d['name']}: **{d['meals_30d']:,}** meals\n"
            return text, context

        # Default response
        text = ("👋 Hello! I'm the REAL.i Meal Demand Assistant. I can help with:\n\n"
                "• Tomorrow's meal predictions\n• Food waste analysis\n"
                "• Location & department insights\n• Prediction accuracy\n"
                "• Meal preparation recommendations\n\n"
                "What would you like to know?")
        return text, None

    def _format_context(self, context: dict) -> str:
        """Format context dict into readable string for LLM."""
        import json
        return json.dumps(context, indent=2, default=str)
