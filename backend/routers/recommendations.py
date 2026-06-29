"""Recommendations Router — AI-generated actionable recommendations."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timezone
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from schemas import RecommendationResponse
from auth import get_current_user_id

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/", response_model=list[RecommendationResponse])
async def get_recommendations(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get AI-generated smart recommendations."""
    from services.recommendation_engine import RecommendationEngine
    engine = RecommendationEngine()
    recs = await engine.generate_recommendations(db)
    return recs
