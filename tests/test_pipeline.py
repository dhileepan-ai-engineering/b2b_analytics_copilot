import os
# Inject a dummy key into the environment so the client initialization succeeds
os.environ["GROQ_API_KEY"] = "mock-key-for-testing-purposes"

import asyncio
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

@pytest.mark.asyncio
@patch("src.agents.client.chat.completions.create")
async def test_successful_strategic_analytics_pipeline(mock_chat_create):
    """
    Validates that a strategic analysis request successfully routes through the
    intent classification engine, executes analytics, and enforces a compliance audit.
    """
    # 1. Build the data response payload for the Router node
    mock_router_response = MagicMock()
    mock_router_response.choices = [MagicMock(message=MagicMock(content="STRATEGIC_ANALYTICS"))]
    mock_router_response.model = "llama-3.3-70b-versatile"
    mock_router_response.usage = MagicMock(prompt_tokens=10, completion_tokens=2, total_tokens=12)

    # 2. Build the data response payload for the Analytics Expert node
    mock_analytics_response = MagicMock()
    mock_analytics_response.choices = [MagicMock(message=MagicMock(content="Executive Insight: Increase promotional funding by 15%."))]
    mock_analytics_response.model = "llama-3.1-8b-instant"
    mock_analytics_response.usage = MagicMock(prompt_tokens=50, completion_tokens=30, total_tokens=80)

    # 3. Build the data response payload for the Compliance Auditor node
    mock_compliance_response = MagicMock()
    mock_compliance_response.choices = [MagicMock(message=MagicMock(content="[AUDIT PASSED]"))]
    mock_compliance_response.model = "llama-3.1-8b-instant"
    mock_compliance_response.usage = MagicMock(prompt_tokens=40, completion_tokens=5, total_tokens=45)

    # 4. Create helper async functions that act as awaitable coroutines
    async def mock_router_call(*args, **kwargs):
        return mock_router_response

    async def mock_analytics_call(*args, **kwargs):
        return mock_analytics_response

    async def mock_compliance_call(*args, **kwargs):
        return mock_compliance_response

    # 5. Use side_effect to route all THREE sequential awaitable calls safely
    mock_chat_create.side_effect = [
        mock_router_call(), 
        mock_analytics_call(), 
        mock_compliance_call()
    ]

    payload = {"query": "Check our current MDF vs VCM thresholds."}
    response = client.post("/v1/execute", json=payload)
    
    # Keeping your debug tracker active just in case
    if response.status_code != 200:
        print("\n--- DETAILED API ERROR OUTPUT ---\n", response.text)
    
    # Assertions
    assert response.status_code == 200
    json_data = response.json()
    
    assert json_data["intent"] == "STRATEGIC_ANALYTICS"
    assert "Executive Insight" in json_data["executive_summary"]
    assert "[Compliance Audit Review]: [AUDIT PASSED]" in json_data["executive_summary"]
    
    # Ensure all telemetry frames from the three nodes exist
    assert "telemetry" in json_data
    assert "router" in json_data["telemetry"]
    assert "execution_node" in json_data["telemetry"]
    assert "compliance_node" in json_data["telemetry"]