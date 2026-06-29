import pytest
import asyncio
import sys
import os
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base, get_db

# Use separate SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_meal_demand.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    # Create all tables in test database
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop all tables after testing
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()
    if os.path.exists("./test_meal_demand.db"):
        try:
            os.remove("./test_meal_demand.db")
        except Exception:
            pass

@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
