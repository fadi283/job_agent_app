import pytest
from unittest.mock import AsyncMock, MagicMock
from app.db.models import Job, ResumeVersion

@pytest.mark.asyncio
async def test_create_resume_success(async_client, mock_db_session):
    # Mock finding the job
    mock_result = MagicMock()
    from datetime import datetime
    mock_job = Job(id=1, title="Software Engineer", created_at=datetime.utcnow())
    mock_result.scalars.return_value.first.return_value = mock_job
    mock_db_session.execute.return_value = mock_result
    
    # Run request
    payload = {
        "job_id": 1,
        "minio_pdf_url": "http://minio/bucket/resume.pdf",
        "minio_docx_url": "http://minio/bucket/resume.docx"
    }
    response = await async_client.post("/api/v1/resumes/", json=payload)
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["job_id"] == 1
    assert data["minio_pdf_url"] == "http://minio/bucket/resume.pdf"
    
    # Verify mock interactions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_resume_job_not_found(async_client, mock_db_session):
    # Mock job not found
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result
    
    # Run request
    payload = {
        "job_id": 999,
        "minio_pdf_url": "http://minio/bucket/resume.pdf"
    }
    response = await async_client.post("/api/v1/resumes/", json=payload)
    
    # Assertions
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
    
    # Verify it didn't save anything
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_awaited()
