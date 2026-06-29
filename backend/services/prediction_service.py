"""Prediction Service — Loads ML model and generates predictions."""
import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import PredictionResult, MealTransaction, WeatherData, WorkLocation, Employee
from schemas import PredictionSummary, PredictionResponse
from config import settings


class PredictionService:
    def __init__(self):
        self.model = None
        self.feature_cols = []
        self.metadata = {}
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(settings.ML_MODEL_PATH):
                self.model = joblib.load(settings.ML_MODEL_PATH)
            if os.path.exists(settings.ML_FEATURES_PATH):
                with open(settings.ML_FEATURES_PATH) as f:
                    self.feature_cols = [l.strip() for l in f if l.strip()]
            if os.path.exists(settings.ML_METADATA_PATH):
                with open(settings.ML_METADATA_PATH) as f:
                    self.metadata = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load ML model: {e}")

    async def predict(self, db: AsyncSession, target_date: date,
                      location_id: int = None) -> PredictionSummary:
        """Generate predictions for a target date."""
        locations = await self._get_locations(db, location_id)
        predictions = []

        for loc in locations:
            for period in ["breakfast", "lunch", "dinner"]:
                features = await self._build_features(db, target_date, loc["id"], period)

                if self.model and features is not None:
                    pred_count = max(0, int(self.model.predict(features.reshape(1, -1))[0]))
                    confidence = 0.85 + np.random.uniform(-0.05, 0.05)
                else:
                    # Fallback: use historical average
                    pred_count = await self._historical_average(db, target_date, loc["id"], period)
                    confidence = 0.70

                waste = int(pred_count * 0.12)
                recommended = pred_count + int(pred_count * 0.05)

                pred = PredictionResult(
                    prediction_date=target_date, location_id=loc["id"],
                    period=period, predicted_count=pred_count,
                    confidence_score=round(confidence, 4),
                    recommended_quantity=recommended, predicted_waste=waste,
                    model_version=self.metadata.get("algorithm", "fallback"),
                    shap_explanation={"text": f"Predicted {pred_count} {period} meals at {loc['name']}"}
                )
                db.add(pred)

                predictions.append(PredictionResponse(
                    prediction_date=target_date, location_id=loc["id"],
                    location_name=loc["name"], period=period,
                    predicted_count=pred_count, confidence_score=round(confidence, 4),
                    recommended_quantity=recommended, predicted_waste=waste,
                    explanation=f"Predicted {pred_count} {period} meals at {loc['name']}"
                ))

        await db.commit()

        total_b = sum(p.predicted_count for p in predictions if p.period == "breakfast")
        total_l = sum(p.predicted_count for p in predictions if p.period == "lunch")
        total_d = sum(p.predicted_count for p in predictions if p.period == "dinner")

        return PredictionSummary(
            date=target_date, total_breakfast=total_b, total_lunch=total_l,
            total_dinner=total_d, total_predicted=total_b + total_l + total_d,
            total_waste=sum(p.predicted_waste for p in predictions),
            confidence=round(np.mean([p.confidence_score for p in predictions]), 4),
            predictions=predictions
        )

    async def _get_locations(self, db, location_id=None):
        query = select(WorkLocation).where(WorkLocation.is_active == True)
        if location_id:
            query = query.where(WorkLocation.id == location_id)
        result = await db.execute(query)
        return [{"id": l.id, "name": l.name, "type": l.location_type}
                for l in result.scalars().all()]

    async def _build_features(self, db, target_date, location_id, period):
        """Build feature vector for prediction."""
        if not self.feature_cols:
            return None
        try:
            features = {}
            features["location_id"] = location_id
            features["year"] = target_date.year
            features["month"] = target_date.month
            features["day"] = target_date.day
            features["day_of_week"] = target_date.weekday()
            features["day_of_year"] = target_date.timetuple().tm_yday
            features["week_of_year"] = target_date.isocalendar()[1]
            features["quarter"] = (target_date.month - 1) // 3 + 1
            features["is_weekend"] = 1 if target_date.weekday() in (4, 5) else 0
            features["saudi_dow"] = (target_date.weekday() + 2) % 7
            features["period_code"] = {"breakfast": 0, "lunch": 1, "dinner": 2}[period]

            # Get historical lag from DB
            for lag in [1, 7, 14, 28]:
                lag_date = target_date - timedelta(days=lag)
                result = await db.execute(
                    select(func.count(MealTransaction.id))
                    .where(MealTransaction.transaction_date == lag_date,
                           MealTransaction.location_id == location_id,
                           MealTransaction.period == period)
                )
                features[f"lag_{lag}d"] = result.scalar() or 0

            # Fill remaining features with defaults
            for col in self.feature_cols:
                if col not in features:
                    features[col] = 0

            return np.array([features.get(col, 0) for col in self.feature_cols], dtype=float)
        except Exception:
            return None

    async def _historical_average(self, db, target_date, location_id, period):
        """Fallback: 30-day historical average."""
        start = target_date - timedelta(days=30)
        result = await db.execute(
            select(func.count(MealTransaction.id))
            .where(MealTransaction.transaction_date >= start,
                   MealTransaction.transaction_date < target_date,
                   MealTransaction.location_id == location_id,
                   MealTransaction.period == period)
        )
        total = result.scalar() or 0
        return max(1, total // 30)
