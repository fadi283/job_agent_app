import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

@pytest.fixture
def mock_db_session():
    # Create an AsyncMock for the database session
    session = AsyncMock()
    # db.add is synchronous
    session.add = MagicMock()
    
    # Mock refresh to populate id and created_at if they are None
    async def mock_refresh(instance):
        if getattr(instance, 'id', None) is None:
            instance.id = 1
        if getattr(instance, 'created_at', None) is None:
            instance.created_at = datetime.utcnow()
    
    session.refresh.side_effect = mock_refresh
    return session

@pytest.fixture
def override_get_db_fixture(mock_db_session):
    async def override_get_db():
        yield mock_db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield mock_db_session
    # Clean up override after test
    app.dependency_overrides.clear()

import pytest_asyncio

@pytest_asyncio.fixture
async def async_client(override_get_db_fixture):
    # Use ASGITransport for testing FastAPI async endpoints
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
