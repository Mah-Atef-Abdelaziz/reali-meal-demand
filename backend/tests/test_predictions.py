import pytest

@pytest.mark.asyncio
async def test_predictions_forecast(client):
    response = await client.get("/api/v1/predictions/forecast?location_id=1&period=lunch")
    assert response.status_code == 200
    data = response.json()
    assert "prediction_date" in data
    assert "location_id" in data
    assert "period" in data
    assert "predicted_count" in data
    assert "confidence_score" in data
    assert "recommended_quantity" in data
    assert "predicted_waste" in data
    assert "shap_explanation" in data
    assert "factors" in data["shap_explanation"]
