from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from app.agents.main_router import MainRouterAgent, Intent
from app.agents.resume_rag import ResumeRAGAgent
from app.agents.interview_prep import InterviewPrepAgent

class AgentState(TypedDict):
    user_input: str
    intent: Optional[Intent]
    job_description: Optional[str]
    past_experience: Optional[str]
    company_info: Optional[str]
    output: Optional[str]

# Instantiate agents
router_agent = MainRouterAgent()
resume_agent = ResumeRAGAgent()
prep_agent = InterviewPrepAgent()

def router_node(state: AgentState) -> AgentState:
    intent = router_agent.classify(state["user_input"])
    return {"intent": intent}

def resume_node(state: AgentState) -> AgentState:
    output = resume_agent.generate_resume(
        state.get("job_description", ""),
        state.get("past_experience", "")
    )
    return {"output": output}

def prep_node(state: AgentState) -> AgentState:
    output = prep_agent.generate_prep(
        state.get("job_description", ""),
        state.get("company_info", "")
    )
    return {"output": output}

def unknown_node(state: AgentState) -> AgentState:
    return {"output": "I'm not sure how to help with that request. Please try specifying if you want to apply for a job, build a resume, or prep for an interview."}

def route_intent(state: AgentState) -> str:
    intent = state.get("intent")
    if intent == Intent.RESUME_GEN:
        return "resume"
    elif intent == Intent.PREP:
        return "prep"
    else:
        # We can route NEW_JOB to unknown for now, or just have it respond nicely
        return "unknown"

# Build Graph
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("resume", resume_node)
builder.add_node("prep", prep_node)
builder.add_node("unknown", unknown_node)

builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    route_intent,
    {
        "resume": "resume",
        "prep": "prep",
        "unknown": "unknown"
    }
)

builder.add_edge("resume", END)
builder.add_edge("prep", END)
builder.add_edge("unknown", END)

app = builder.compile()
