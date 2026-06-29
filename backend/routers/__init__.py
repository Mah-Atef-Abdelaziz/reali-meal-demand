"""Routers package — aggregates all API route modules."""
from .auth import router as auth_router
from .predictions import router as predictions_router
from .dashboard import router as dashboard_router
from .chatbot import router as chatbot_router
from .employees import router as employees_router
from .recommendations import router as recommendations_router
from .reports import router as reports_router

all_routers = [
    auth_router,
    predictions_router,
    dashboard_router,
    chatbot_router,
    employees_router,
    recommendations_router,
    reports_router,
]
