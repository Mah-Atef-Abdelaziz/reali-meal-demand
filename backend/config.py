"""
Application Configuration — Environment-based settings using Pydantic.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = "REAL.i Meal Demand AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Database (SQLite by default for zero-dependency local dev)
    DATABASE_URL: str = "sqlite+aiosqlite:///./meal_demand.db"
    DATABASE_SYNC_URL: str = "sqlite:///./meal_demand.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT Auth
    JWT_SECRET_KEY: str = "reali-meal-demand-secret-key-change-in-production-2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OpenAI / LLM
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    USE_LOCAL_LLM: bool = False  # Auto-fallback if no OpenAI key

    # ChromaDB
    CHROMA_PERSIST_DIR: str = os.path.join(os.path.dirname(__file__), "chroma_db")

    # ML Model
    ML_MODEL_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                       "ml", "models", "best_model.joblib")
    ML_METADATA_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "ml", "models", "model_metadata.json")
    ML_FEATURES_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          "ml", "processed", "feature_cols.txt")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"

    @property
    def cors_origins_list(self) -> list:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def use_openai(self) -> bool:
        return bool(self.OPENAI_API_KEY) and not self.USE_LOCAL_LLM

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
