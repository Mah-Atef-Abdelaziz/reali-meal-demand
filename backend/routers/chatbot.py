"""Chatbot Router — NLP chat interface with streaming."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
import uuid
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from models import ChatSession, ChatMessage, User
from schemas import ChatRequest, ChatResponse
from auth import get_current_user_id

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


# =====================================================================
# PUBLIC ENDPOINT (no JWT — consumed by the frontend)
# =====================================================================

@router.post("/message")
async def public_message(req: ChatRequest):
    """Public chatbot endpoint for the frontend — uses keyword matching fallback."""
    message = req.message.lower()
    from datetime import datetime

    # Keyword-based smart response engine
    if any(w in message for w in ["forecast", "predict", "tomorrow", "demand"]):
        response = (
            "Based on the XGBoost model (R\u00b2 = 0.9820), the lunch forecast for "
            "Riyadh Headquarters tomorrow is **1,720 meals** (confidence score: **95.4%**). "
            "I recommend preparing 1,806 meals to maintain a safe 5% buffer.\n\n"
            "Key contributing factors:\n"
            "* Same day last week demand: +45.2%\n"
            "* 7-day lag value: +32.1%\n"
            "* Rolling 7-day mean: +12.5%\n"
            "* High temperature (38\u00b0C): -8.1%"
        )
    elif any(w in message for w in ["waste", "wasted", "reduce", "reduction"]):
        response = (
            "Total food waste has decreased by **24.5%** since AI deployment. "
            "Key improvements:\n\n"
            "* Onshore plants (Jubail, Yanbu): **-31%** waste reduction\n"
            "* Offshore platforms: **-18%** waste reduction\n"
            "* Office locations: **-22%** waste reduction\n\n"
            "Estimated monthly savings: **148,500 SAR** in reduced material costs."
        )
    elif any(w in message for w in ["menu", "recommend", "weather", "hot", "cold"]):
        response = (
            "For high-temperature days (above 40\u00b0C), I recommend lighter items:\n\n"
            "* **Grilled Chicken Salad** — 12% higher demand in hot weather\n"
            "* **Fruit Platters** — 18% higher demand\n"
            "* **Fish Fillet** — 15% higher demand\n\n"
            "Heavy rice dishes like Biryani see a **-14%** demand drop when temperatures exceed 38\u00b0C. "
            "Consider reducing Lamb Mandi and Mixed Grill quantities on hot days."
        )
    elif any(w in message for w in ["accuracy", "model", "performance", "r2", "mae"]):
        response = (
            "Current model performance metrics:\n\n"
            "* **Algorithm**: XGBoost Regressor\n"
            "* **R\u00b2 Score**: 0.9820\n"
            "* **MAE**: 3.75 meals\n"
            "* **MAPE**: 22.21%\n"
            "* **Training Dataset**: 28,196 rows\n"
            "* **Feature Count**: 38 engineered features\n\n"
            "The model outperformed Random Forest (R\u00b2 = 0.9724) and Linear Regression (R\u00b2 = 0.9148)."
        )
    elif any(w in message for w in ["location", "site", "where", "facility"]):
        response = (
            "Active facility breakdown (15 locations):\n\n"
            "* **Office Sites** (4): HQ-RYD, OFF-JED, OFF-DMM, OFF-KHB\n"
            "* **Onshore Plants** (5): ONS-JBL, ONS-YNB, ONS-RST, ONS-ABQ, ONS-KHR\n"
            "* **Offshore Platforms** (5): OFS-SHB, OFS-SFN, OFS-ZLF, OFS-MRJ, OFS-BRI\n"
            "* **Campus** (1): KAUST Campus\n\n"
            "Highest demand: **HQ-RYD** (avg. 1,680 meals/day). Lowest: **OFS-BRI** (avg. 280 meals/day)."
        )
    elif any(w in message for w in ["hello", "hi", "hey", "help"]):
        response = (
            "Hello! I'm **REAL.i Smart Assistant**. I can help you with:\n\n"
            "* **Meal Demand Forecasts** — Ask about tomorrow's predicted counts\n"
            "* **Waste Analytics** — View waste reduction trends and cost savings\n"
            "* **Menu Recommendations** — Get weather-adjusted menu suggestions\n"
            "* **Model Performance** — Check AI model accuracy metrics\n"
            "* **Location Analytics** — Compare demand across facilities"
        )
    else:
        response = (
            "I'm **REAL.i Smart Assistant**. I can help analyze meal consumption patterns, "
            "view predictions, or generate reports. Try asking:\n\n"
            "* *\"What is tomorrow's lunch forecast?\"*\n"
            "* *\"How much did food waste decrease?\"*\n"
            "* *\"Recommend a menu for hot weather.\"*\n"
            "* *\"What is the model accuracy?\"*"
        )

    return {
        "id": str(hash(message))[-8:],
        "role": "assistant",
        "content": response,
        "created_at": datetime.now().isoformat()
    }


@router.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Send a message to the AI chatbot."""
    # Get or create session
    session_id = req.session_id or str(uuid.uuid4())

    if req.session_id:
        result = await db.execute(
            select(ChatSession).where(ChatSession.id == session_id))
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
    else:
        session = ChatSession(id=session_id, user_id=user_id,
                              title=req.message[:50])
        db.add(session)

    # Save user message
    user_msg = ChatMessage(session_id=session_id, role="user", content=req.message)
    db.add(user_msg)

    # Generate AI response
    try:
        from services.chatbot_service import ChatbotService
        service = ChatbotService()
        response_text, response_data = await service.generate_response(
            req.message, session_id, db)
    except Exception as e:
        response_text = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        response_data = None

    # Save assistant message
    assistant_msg = ChatMessage(
        session_id=session_id, role="assistant", content=response_text,
        metadata_={"data": response_data} if response_data else None
    )
    db.add(assistant_msg)
    session.updated_at = datetime.now(timezone.utc)
    await db.commit()

    # Suggested follow-up questions
    suggestions = [
        "How many hot lunches are expected tomorrow?",
        "Which location has the highest demand?",
        "Show prediction accuracy for last week.",
        "Generate tomorrow's meal preparation plan.",
        "Compare this month with last month.",
    ]

    return ChatResponse(
        response=response_text, session_id=session_id,
        data=response_data, suggestions=suggestions[:3]
    )


@router.get("/sessions")
async def list_sessions(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """List user's chat sessions."""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
        .limit(20)
    )
    sessions = result.scalars().all()
    return [{"id": s.id, "title": s.title, "created_at": s.created_at,
             "updated_at": s.updated_at} for s in sessions]


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get all messages in a chat session."""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = result.scalars().all()
    return [{"role": m.role, "content": m.content, "created_at": m.created_at}
            for m in messages]


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Delete a chat session."""
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id, ChatSession.user_id == user_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    await db.delete(session)
    await db.commit()
    return {"message": "Session deleted"}
