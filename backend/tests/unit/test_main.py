import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """
    Test the health check endpoint to ensure it returns 200 OK
    and the expected JSON status.
    """
    # Note: For testing FastAPI with async endpoints, it's recommended to use httpx.AsyncClient
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health1")
        
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
