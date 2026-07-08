from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.models import Job, ResumeVersion
from app.api.schemas import ResumeVersionCreate, ResumeVersionResponse, ResumeVersionUpdate

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

@router.patch("/{resume_id}", response_model=ResumeVersionResponse)
async def update_resume_version(resume_id: int, resume_in: ResumeVersionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResumeVersion).filter(ResumeVersion.id == resume_id))
    resume = result.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume version not found")
        
    update_data = resume_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resume, field, value)
        
    await db.commit()
    await db.refresh(resume)
    return resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_version(resume_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResumeVersion).filter(ResumeVersion.id == resume_id))
    resume = result.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume version not found")
        
    await db.delete(resume)
    await db.commit()
    return None
