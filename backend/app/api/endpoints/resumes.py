from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.models import Job, ResumeVersion
from app.api.schemas import ResumeVersionCreate, ResumeVersionResponse

router = APIRouter()

@router.post("/", response_model=ResumeVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_resume_version(resume_in: ResumeVersionCreate, db: AsyncSession = Depends(get_db)):
    # Check if job exists
    result = await db.execute(select(Job).filter(Job.id == resume_in.job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    new_resume = ResumeVersion(**resume_in.model_dump())
    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)
    return new_resume
