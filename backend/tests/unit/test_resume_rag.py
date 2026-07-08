import pytest
from unittest.mock import patch, MagicMock
from app.agents.resume_rag import ResumeRAGAgent
from langchain_openai import ChatOpenAI

def test_resume_rag_generate():
    with patch.object(ChatOpenAI, 'invoke') as mock_invoke:
        mock_msg = MagicMock()
        mock_msg.content = "TAILORED RESUME CONTENT"
        mock_invoke.return_value = mock_msg
        
        agent = ResumeRAGAgent()
        
        job_description = "Looking for a Python backend engineer with FastAPI experience."
        past_experience = "I have 5 years of Python experience building APIs."
        
        tailored_text = agent.generate_resume(job_description, past_experience)
        
        assert tailored_text == "TAILORED RESUME CONTENT"
        mock_invoke.assert_called_once()
