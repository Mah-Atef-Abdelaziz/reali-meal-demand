"""
Database setup — SQLAlchemy async engine and session management.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from config import settings


# Determine if we are using SQLite
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# Fix asyncpg SSL: asyncpg doesn't support ?sslmode=require, use ssl=True instead
db_url = settings.DATABASE_URL
if not is_sqlite and "sslmode=" in db_url:
    db_url = db_url.split("?sslmode=")[0]  # Strip sslmode param

# Async engine for FastAPI
engine_kwargs = {"echo": settings.DEBUG}
if not is_sqlite:
    engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "connect_args": {"ssl": True},
    })
else:
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False}
    })

async_engine = create_async_engine(
    db_url,
    **engine_kwargs
)

# Async session factory
async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Sync engine (for migrations, data loading)
sync_engine_kwargs = {}
if is_sqlite:
    sync_engine_kwargs["connect_args"] = {"check_same_thread": False}
sync_engine = create_engine(settings.DATABASE_SYNC_URL, echo=False, **sync_engine_kwargs)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


async def get_db() -> AsyncSession:
    """Dependency injection for database sessions."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables (development only)."""
    import models  # Register models on Base.metadata
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections."""
    await async_engine.dispose()
