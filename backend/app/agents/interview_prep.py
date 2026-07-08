import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class InterviewPrepAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=api_key)
        
        self.prompt = PromptTemplate.from_template(
            """You are an expert technical interview coach. 
Your goal is to provide tailored interview preparation and strategy based on the job description and company information.
Include potential questions, strategies, and key areas to focus on.

Job Description:
{job_description}

Company Information:
{company_info}

Interview Preparation Material:"""
        )

    def generate_prep(self, job_description: str, company_info: str) -> str:
        chain = self.prompt | self.llm
        
        response = chain.invoke({
            "job_description": job_description,
            "company_info": company_info
        })
        
        return response.content.strip()
