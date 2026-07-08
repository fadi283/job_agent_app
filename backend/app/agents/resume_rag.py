import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class ResumeRAGAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=api_key)
        
        self.prompt = PromptTemplate.from_template(
            """You are an expert resume writer. 
Your goal is to tailor the candidate's past experience to match the provided job description.
Do not invent or hallucinate any experience. Only use what is provided in the past experience.

Job Description:
{job_description}

Candidate's Past Experience:
{past_experience}

Tailored Resume Section:"""
        )

    def generate_resume(self, job_description: str, past_experience: str) -> str:
        chain = self.prompt | self.llm
        
        response = chain.invoke({
            "job_description": job_description,
            "past_experience": past_experience
        })
        
        return response.content.strip()
