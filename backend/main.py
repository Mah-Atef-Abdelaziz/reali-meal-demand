"""
REAL.i Meal Demand AI — FastAPI Application Entry Point
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging

from config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL),
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("meal_demand_ai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown lifecycle."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    # Startup
    try:
        from database import init_db
        await init_db()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning(f"Database init skipped: {e}")
    yield
    # Shutdown
    try:
        from database import close_db
        await close_db()
        logger.info("Database connections closed")
    except Exception:
        pass


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered meal demand prediction and smart assistant system for reducing food waste.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allow all origins for public API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = f"{duration:.3f}"
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred.", "error": str(exc)},
    )


# Register routers
from routers import all_routers
for router in all_routers:
    app.include_router(router, prefix=settings.API_PREFIX)


# Health check endpoints
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/ready", tags=["System"])
async def readiness_check():
    """Check if all dependencies are ready."""
    checks = {"database": False, "ml_model": False}

    # Database check
    try:
        from database import async_session_factory
        async with async_session_factory() as session:
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
            checks["database"] = True
    except Exception:
        pass

    # ML model check
    try:
        checks["ml_model"] = os.path.exists(settings.ML_MODEL_PATH)
    except Exception:
        pass

    all_ready = all(checks.values())
    return {"ready": all_ready, "checks": checks}


@app.get("/", tags=["System"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "api": settings.API_PREFIX,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
