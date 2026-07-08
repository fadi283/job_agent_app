from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db.models import Job
from app.api.schemas import JobCreate, JobResponse, JobUpdate

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job_in: JobCreate, db: AsyncSession = Depends(get_db)):
    new_job = Job(**job_in.model_dump())
    db.add(new_job)
    await db.commit()
    
    # Query the job again to eagerly load the resume_versions relationship
    result = await db.execute(
        select(Job).options(selectinload(Job.resume_versions)).filter(Job.id == new_job.id)
    )
    new_job_loaded = result.scalars().first()
    
    return new_job_loaded

@router.get("/", response_model=List[JobResponse])
async def read_jobs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).options(selectinload(Job.resume_versions)).offset(skip).limit(limit))
    jobs = result.scalars().all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def read_job(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).options(selectinload(Job.resume_versions)).filter(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(job_id: int, job_in: JobUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).options(selectinload(Job.resume_versions)).filter(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)
        
    await db.commit()
    await db.refresh(job)
    
    # Reload with relationships
    result = await db.execute(select(Job).options(selectinload(Job.resume_versions)).filter(Job.id == job_id))
    return result.scalars().first()

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).filter(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    await db.delete(job)
    await db.commit()
    return None
