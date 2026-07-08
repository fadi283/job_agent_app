import pytest
from unittest.mock import AsyncMock, MagicMock
from app.db.models import Job

@pytest.mark.asyncio
async def test_create_job(async_client, mock_db_session):
    # Setup mock
    # db.add is synchronous, db.commit is async, db.refresh is async
    
    # Mock db.execute for the relationship reload
    mock_result = MagicMock()
    from datetime import datetime
    mock_job = Job(id=1, title="Software Engineer", company="Tech Corp", created_at=datetime.utcnow())
    mock_result.scalars.return_value.first.return_value = mock_job
    mock_db_session.execute.return_value = mock_result
    
    # Run request
    payload = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "job_url": "http://example.com",
        "status": "applied",
        "manual_notes": "Great opportunity"
    }
    response = await async_client.post("/api/v1/jobs/", json=payload)
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Software Engineer"
    assert data["company"] == "Tech Corp"
    
    # Verify mock interactions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_read_jobs(async_client, mock_db_session):
    # Setup mock for db.execute(select(...))
    mock_result = MagicMock()
    from datetime import datetime
    # Mock jobs to return from scalars().all()
    mock_job_1 = Job(id=1, title="Job 1", company="Comp 1", created_at=datetime.utcnow())
    mock_job_2 = Job(id=2, title="Job 2", company="Comp 2", created_at=datetime.utcnow())
    mock_result.scalars.return_value.all.return_value = [mock_job_1, mock_job_2]
    
    mock_db_session.execute.return_value = mock_result
    
    # Run request
    response = await async_client.get("/api/v1/jobs/")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Job 1"
    assert data[1]["title"] == "Job 2"

@pytest.mark.asyncio
async def test_read_job_found(async_client, mock_db_session):
    # Setup mock
    mock_result = MagicMock()
    from datetime import datetime
    mock_job = Job(id=1, title="Job 1", company="Comp 1", created_at=datetime.utcnow())
    mock_result.scalars.return_value.first.return_value = mock_job
    mock_db_session.execute.return_value = mock_result
    
    # Run request
    response = await async_client.get("/api/v1/jobs/1")
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["title"] == "Job 1"

@pytest.mark.asyncio
async def test_read_job_not_found(async_client, mock_db_session):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result
    
    # Run request
    response = await async_client.get("/api/v1/jobs/999")
    
    # Assertions
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
