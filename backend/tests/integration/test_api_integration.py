import pytest
from unittest.mock import MagicMock
from app.db.models import Job, ResumeVersion
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_integration_jobs_workflow(async_client, mock_db_session):
    # 1. POST /api/v1/jobs/
    mock_result_create = MagicMock()
    mock_job = Job(id=1, title="Software Engineer", company="Tech Corp", created_at=datetime.now(timezone.utc))
    mock_result_create.scalars.return_value.first.return_value = mock_job
    mock_db_session.execute.return_value = mock_result_create
    
    payload = {
        "title": "Software Engineer",
        "company": "Tech Corp"
    }
    response = await async_client.post("/api/v1/jobs/", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == 1
    
    # 2. GET /api/v1/jobs/
    mock_result_list = MagicMock()
    mock_result_list.scalars.return_value.all.return_value = [mock_job]
    mock_db_session.execute.return_value = mock_result_list
    
    response = await async_client.get("/api/v1/jobs/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # 3. PATCH /api/v1/jobs/1
    mock_result_patch = MagicMock()
    mock_updated_job = Job(id=1, title="Senior Software Engineer", company="Tech Corp", created_at=datetime.now(timezone.utc))
    mock_result_patch.scalars.return_value.first.return_value = mock_updated_job
    mock_db_session.execute.return_value = mock_result_patch
    
    update_payload = {"title": "Senior Software Engineer"}
    response = await async_client.patch("/api/v1/jobs/1", json=update_payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Senior Software Engineer"
    
    # 4. DELETE /api/v1/jobs/1
    mock_result_delete = MagicMock()
    mock_result_delete.scalars.return_value.first.return_value = mock_updated_job
    mock_db_session.execute.return_value = mock_result_delete
    
    response = await async_client.delete("/api/v1/jobs/1")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_integration_resumes_workflow(async_client, mock_db_session):
    # 1. POST /api/v1/resumes/
    mock_result_job = MagicMock()
    mock_job = Job(id=1, title="Software Engineer", created_at=datetime.now(timezone.utc))
    mock_result_job.scalars.return_value.first.return_value = mock_job
    
    # When resume is created, it first checks if job exists, then refreshes. 
    # We'll just let the mock return mock_job for the first execute.
    mock_db_session.execute.return_value = mock_result_job
    
    payload = {
        "job_id": 1,
        "minio_pdf_url": "s3://bucket/resume.pdf"
    }
    response = await async_client.post("/api/v1/resumes/", json=payload)
    assert response.status_code == 201
    assert response.json()["job_id"] == 1
    
    # 2. PATCH /api/v1/resumes/1
    mock_result_resume = MagicMock()
    mock_resume = ResumeVersion(id=1, job_id=1, minio_pdf_url="s3://bucket/resume.pdf", minio_docx_url="s3://bucket/resume.docx", created_at=datetime.now(timezone.utc))
    mock_result_resume.scalars.return_value.first.return_value = mock_resume
    mock_db_session.execute.return_value = mock_result_resume
    
    update_payload = {"minio_docx_url": "s3://bucket/resume.docx"}
    response = await async_client.patch("/api/v1/resumes/1", json=update_payload)
    assert response.status_code == 200
    assert response.json()["minio_docx_url"] == "s3://bucket/resume.docx"
    
    # 3. DELETE /api/v1/resumes/1
    response = await async_client.delete("/api/v1/resumes/1")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
