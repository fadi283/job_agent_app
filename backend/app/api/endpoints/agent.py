from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.schemas import AgentRequest, AgentResponse
from app.agents.graph import app as graph_app
from app.db.session import get_db
from app.db.models import Job

router = APIRouter()

@router.post("/", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest, db: AsyncSession = Depends(get_db)):
    # If job_id is provided, try to fetch job from DB to populate context
    if request.job_id:
        result = await db.execute(select(Job).filter(Job.id == request.job_id))
        job = result.scalars().first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Override with DB data if not manually provided
        if not request.job_description and job.job_description:
            request.job_description = job.job_description
        if not request.company_info and job.company:
            request.company_info = job.company

    # Convert request to state dict
    state_input = {
        "user_input": request.user_input,
    }
    if request.job_description:
        state_input["job_description"] = request.job_description
    if request.company_info:
        state_input["company_info"] = request.company_info
    if request.past_experience:
        state_input["past_experience"] = request.past_experience
        
    result = graph_app.invoke(state_input)
    
    return AgentResponse(output=result.get("output", "No response generated."))
