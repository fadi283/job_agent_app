from fastapi import APIRouter
from app.api.schemas import AgentRequest, AgentResponse
from app.agents.graph import app as graph_app

router = APIRouter()

@router.post("/", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
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
