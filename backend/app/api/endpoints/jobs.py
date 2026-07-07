from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db.models import Job
from app.api.schemas import JobCreate, JobResponse

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job_in: JobCreate, db: AsyncSession = Depends(get_db)):
    new_job = Job(**job_in.model_dump())
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job

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
