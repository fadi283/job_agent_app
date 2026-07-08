from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

# --- ResumeVersion Schemas ---
class ResumeVersionBase(BaseModel):
    minio_pdf_url: Optional[str] = None
    minio_docx_url: Optional[str] = None

class ResumeVersionCreate(ResumeVersionBase):
    job_id: int

class ResumeVersionUpdate(BaseModel):
    minio_pdf_url: Optional[str] = None
    minio_docx_url: Optional[str] = None

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
    job_description: Optional[str] = None
    status: Optional[str] = "applied"
    manual_notes: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    job_url: Optional[str] = None
    status: Optional[str] = None
    manual_notes: Optional[str] = None

class JobResponse(JobBase):
    id: int
    created_at: datetime
    resume_versions: List[ResumeVersionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# --- Agent Schemas ---
class AgentRequest(BaseModel):
    user_input: str
    job_id: Optional[int] = None
    job_description: Optional[str] = None
    company_info: Optional[str] = None
    past_experience: Optional[str] = None

class AgentResponse(BaseModel):
    output: str
