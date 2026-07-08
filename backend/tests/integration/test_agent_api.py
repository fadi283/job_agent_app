import pytest
from unittest.mock import patch

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
