import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_agent_endpoint(async_client):
    # Mock the graph execution to prevent actual LLM calls
    mock_output = {"output": "This is a mocked agent response"}
    
    with patch("app.api.endpoints.agent.graph_app.invoke", return_value=mock_output) as mock_invoke:
        payload = {
            "user_input": "Help me build a resume",
            "job_description": "Software Engineer at Tech Corp",
            "past_experience": "Worked as a developer for 3 years."
        }
        
        response = await async_client.post("/api/v1/agent/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert data["output"] == "This is a mocked agent response"
        
        # Verify it was called with the correct state dictionary
        mock_invoke.assert_called_once_with(payload)

@pytest.mark.asyncio
async def test_agent_endpoint_with_job_id(async_client, mock_db_session):
    mock_output = {"output": "This is a mocked agent response for a specific job"}
    
    # Create a mock job to be returned by db.execute
    class MockJob:
        id = 1
        title = "Backend Dev"
        company = "Startup Inc"
        job_description = "We need a python expert."
    
    mock_job = MockJob()
    
    # Mock the result of db.execute(...).scalars().first()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = mock_job
    mock_result.scalars.return_value = mock_scalars
    mock_db_session.execute.return_value = mock_result

    # Now, test the agent endpoint using this job_id
    with patch("app.api.endpoints.agent.graph_app.invoke", return_value=mock_output) as mock_invoke:
        agent_payload = {
            "user_input": "Help me build a resume for this job",
            "job_id": 1
        }
        
        response = await async_client.post("/api/v1/agent/", json=agent_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["output"] == "This is a mocked agent response for a specific job"
        
        # Verify the agent was invoked with the injected context from DB
        expected_state = {
            "user_input": "Help me build a resume for this job",
            "job_description": "We need a python expert.",
            "company_info": "Startup Inc"
        }
        mock_invoke.assert_called_once_with(expected_state)
