from enum import Enum
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class Intent(Enum):
    NEW_JOB = "NEW_JOB"
    RESUME_GEN = "RESUME_GEN"
    PREP = "PREP"
    UNKNOWN = "UNKNOWN"

class MainRouterAgent:
    def __init__(self):
        # We use a dummy API key for instantiation so it doesn't crash if ENV is missing during tests
        api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)
        
        self.prompt = PromptTemplate.from_template(
            """You are a routing agent for a Job Application Assistant.
Classify the user's intent into exactly one of the following categories:
- NEW_JOB: The user wants to apply for a new job, provided a job link, or wants to save a job description.
- RESUME_GEN: The user wants to generate, compile, or tailor a resume for an existing job.
- PREP: The user wants interview preparation, a study plan, or gap analysis.
- UNKNOWN: The request doesn't fit any of the above.

Respond ONLY with the category name (e.g. NEW_JOB).

User Input: {user_input}
Intent:"""
        )

    def classify(self, text: str) -> Intent:
        # Create the chain
        chain = self.prompt | self.llm
        
        # Invoke the LLM
        response = chain.invoke({"user_input": text})
        
        # Parse result
        content = response.content.strip().upper()
        try:
            return Intent(content)
        except ValueError:
            return Intent.UNKNOWN
