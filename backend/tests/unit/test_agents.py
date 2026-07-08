import pytest
from unittest.mock import patch, MagicMock
from app.agents.main_router import MainRouterAgent, Intent
from langchain_openai import ChatOpenAI

def test_router_agent_classify_new_job():
    with patch.object(ChatOpenAI, 'invoke') as mock_invoke:
        mock_msg = MagicMock()
        mock_msg.content = "NEW_JOB"
        mock_invoke.return_value = mock_msg
        
        agent = MainRouterAgent()
        intent = agent.classify("I want to apply for this job: http://linkedin.com/job")
        
        assert intent == Intent.NEW_JOB
        mock_invoke.assert_called_once()

def test_router_agent_classify_resume_gen():
    with patch.object(ChatOpenAI, 'invoke') as mock_invoke:
        mock_msg = MagicMock()
        mock_msg.content = "RESUME_GEN"
        mock_invoke.return_value = mock_msg
        
        agent = MainRouterAgent()
        intent = agent.classify("Please generate a tailored resume for job id 5")
        assert intent == Intent.RESUME_GEN

def test_router_agent_classify_prep():
    with patch.object(ChatOpenAI, 'invoke') as mock_invoke:
        mock_msg = MagicMock()
        mock_msg.content = "PREP"
        mock_invoke.return_value = mock_msg
        
        agent = MainRouterAgent()
        intent = agent.classify("I need an interview study plan")
        assert intent == Intent.PREP
