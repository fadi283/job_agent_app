from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

# --- ResumeVersion Schemas ---
class ResumeVersionBase(BaseModel):
    minio_pdf_url: Optional[str] = None
    minio_docx_url: Optional[str] = None

class ResumeVersionCreate(ResumeVersionBase):
    job_id: int

class ResumeVersionResponse(ResumeVersionBase):
    id: int
    job_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Job Schemas ---
class JobBase(BaseModel):
    title: str
    company: str
    job_url: Optional[str] = None
    status: Optional[str] = "applied"
    manual_notes: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    created_at: datetime
    resume_versions: List[ResumeVersionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
