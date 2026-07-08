import pytest
from unittest.mock import patch, MagicMock
from app.agents.interview_prep import InterviewPrepAgent
from langchain_openai import ChatOpenAI

def test_interview_prep_generate():
    with patch.object(ChatOpenAI, 'invoke') as mock_invoke:
        mock_msg = MagicMock()
        mock_msg.content = "INTERVIEW PREP MATERIAL"
        mock_invoke.return_value = mock_msg
        
        agent = InterviewPrepAgent()
        
        job_description = "Looking for a Python backend engineer with FastAPI experience."
        company_info = "Tech startup focused on AI."
        
        prep_material = agent.generate_prep(job_description, company_info)
        
        assert prep_material == "INTERVIEW PREP MATERIAL"
        mock_invoke.assert_called_once()
