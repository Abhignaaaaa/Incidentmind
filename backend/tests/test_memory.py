import pytest
from unittest.mock import patch, MagicMock
import httpx
from app.memory.service import MemoryService
from app.memory.hindsight import HindsightClient
from app.config import settings

@pytest.mark.asyncio
async def test_memory_retain_recall_fallback():
    # Testing the local fallback explicitly by forcing credentials to be empty
    service = MemoryService()
    service.client.api_key = ""
    service.client.bank_id = ""
    service.client.local_memory = []
    
    await service.retain("Test redis issue memory")
    memories = await service.recall("redis")
    assert len(memories) > 0
    assert "Test redis issue memory" in memories[0].content

@pytest.mark.asyncio
@patch("app.memory.hindsight.httpx.AsyncClient.post")
async def test_hindsight_real_http_calls(mock_post):
    client = HindsightClient()
    client.url = "https://api.hindsight.vectorize.io"
    client.api_key = "test-key"
    client.bank_id = "test-bank"
    client.headers = {"Authorization": "Bearer test-key", "Content-Type": "application/json"}
    
    # Mock Retain Response
    mock_retain_response = MagicMock()
    mock_retain_response.raise_for_status = MagicMock(return_value=None)
    mock_post.return_value = mock_retain_response
    
    retain_id = await client.store("Database down", metadata={})
    assert retain_id == "hindsight-retained-id"
    
    mock_post.assert_called_with(
        "https://api.hindsight.vectorize.io/v1/default/banks/test-bank/memories",
        json={"items": [{"content": "Database down"}]},
        headers=client.headers,
        timeout=5.0
    )
    
    # Mock Recall Response
    mock_recall_response = MagicMock()
    mock_recall_response.raise_for_status = MagicMock(return_value=None)
    mock_recall_response.json = MagicMock(return_value={
        "results": [
            {"text": "Database was down because of OOM"}
        ]
    })
    mock_post.return_value = mock_recall_response
    
    memories = await client.search("Database")
    assert len(memories) == 1
    assert memories[0].content == "Database was down because of OOM"
    
    mock_post.assert_called_with(
        "https://api.hindsight.vectorize.io/v1/default/banks/test-bank/memories/recall",
        json={"query": "Database"},
        headers=client.headers,
        timeout=5.0
    )

@pytest.mark.asyncio
@pytest.mark.skipif(not settings.HINDSIGHT_API_KEY, reason="No Hindsight API key configured for real integration test")
async def test_hindsight_real_integration():
    # Only runs if HINDSIGHT_API_KEY is configured
    service = MemoryService()
    memories = await service.recall("Redis connection failures")
    assert isinstance(memories, list)
