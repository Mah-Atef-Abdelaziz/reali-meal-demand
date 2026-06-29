import pytest

@pytest.mark.asyncio
async def test_chatbot_message_fallback(client):
    response = await client.post("/api/v1/chatbot/message", json={"message": "hello"})
    assert response.status_code == 200
    data = response.json()
    assert "role" in data
    assert "content" in data
    assert "assistant" == data["role"]

@pytest.mark.asyncio
async def test_chatbot_message_forecast(client):
    response = await client.post("/api/v1/chatbot/message", json={"message": "what is tomorrow's forecast?"})
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "1,720" in data["content"] or "assistant" == data["role"]
