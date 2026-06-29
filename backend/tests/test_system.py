import pytest

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

@pytest.mark.asyncio
async def test_readiness_check(client):
    response = await client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data
    assert "checks" in data
