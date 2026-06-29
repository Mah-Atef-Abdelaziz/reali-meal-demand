import pytest

@pytest.mark.asyncio
async def test_dashboard_summary(client):
    response = await client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
    assert "average_confidence" in data
    assert "saved_cost_sar" in data
    assert "waste_reduction_percent" in data

@pytest.mark.asyncio
async def test_dashboard_periods(client):
    response = await client.get("/api/v1/dashboard/periods")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "period" in data[0]
    assert "count" in data[0]

@pytest.mark.asyncio
async def test_dashboard_waste(client):
    response = await client.get("/api/v1/dashboard/waste")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "date" in data[0]
    assert "prepared" in data[0]
    assert "wasted" in data[0]
