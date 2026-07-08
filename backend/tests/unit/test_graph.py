import pytest
from unittest.mock import patch, MagicMock
from app.agents.graph import app as graph_app
from app.agents.main_router import Intent

@patch("app.agents.graph.MainRouterAgent.classify")
def test_graph_routes_to_resume_gen(mock_classify):
    mock_classify.return_value = Intent.RESUME_GEN
    
    with patch("app.agents.graph.ResumeRAGAgent.generate_resume") as mock_resume:
        mock_resume.return_value = "Mocked Resume"
        
        initial_state = {
            "user_input": "Create my resume",
            "job_description": "Software Engineer",
            "past_experience": "5 years Python",
            "company_info": ""
        }
        
        final_state = graph_app.invoke(initial_state)
        
        assert final_state["intent"] == Intent.RESUME_GEN
        assert final_state["output"] == "Mocked Resume"
        mock_classify.assert_called_once_with("Create my resume")
        mock_resume.assert_called_once_with("Software Engineer", "5 years Python")

@patch("app.agents.graph.MainRouterAgent.classify")
def test_graph_routes_to_prep(mock_classify):
    mock_classify.return_value = Intent.PREP
    
    with patch("app.agents.graph.InterviewPrepAgent.generate_prep") as mock_prep:
        mock_prep.return_value = "Mocked Prep"
        
        initial_state = {
            "user_input": "Prep me for Google",
            "job_description": "Software Engineer",
            "past_experience": "",
            "company_info": "Google"
        }
        
        final_state = graph_app.invoke(initial_state)
        
        assert final_state["intent"] == Intent.PREP
        assert final_state["output"] == "Mocked Prep"
        mock_classify.assert_called_once_with("Prep me for Google")
        mock_prep.assert_called_once_with("Software Engineer", "Google")

@patch("app.agents.graph.MainRouterAgent.classify")
def test_graph_routes_to_unknown(mock_classify):
    mock_classify.return_value = Intent.UNKNOWN
    
    initial_state = {
        "user_input": "Hello world",
        "job_description": "",
        "past_experience": "",
        "company_info": ""
    }
    
    final_state = graph_app.invoke(initial_state)
    
    assert final_state["intent"] == Intent.UNKNOWN
    assert "I'm not sure how to help" in final_state["output"]
    mock_classify.assert_called_once_with("Hello world")
