import httpx
from app.config import settings
from app.logging import logger
from .schemas import MemoryRecord

class HindsightClient:
    """
    HTTP Client for the real Hindsight API.
    In Phase 1, we use an in-memory fallback if the real API fails or isn't configured.
    """
    def __init__(self):
        self.url = settings.HINDSIGHT_URL.rstrip('/')
        self.api_key = settings.HINDSIGHT_API_KEY
        self.bank_id = settings.HINDSIGHT_BANK_ID
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {}
        # Fallback memory store if real API is down
        self.local_memory = []

    async def store(self, text: str, metadata: dict) -> str:
        if not self.api_key or not self.bank_id:
            logger.warning("No Hindsight API key or bank ID configured, using local fallback.")
            self.local_memory.append({"content": text, "metadata": metadata})
            return "local-id"
        
        # Real Hindsight API call
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "items": [
                        {
                            "content": text
                            # Not sending arbitrary metadata since RetainRequest schema only officially supports specific fields (context, document_id, timestamp)
                        }
                    ]
                }
                response = await client.post(
                    f"{self.url}/v1/default/banks/{self.bank_id}/memories",
                    json=payload,
                    headers=self.headers,
                    timeout=5.0
                )
                response.raise_for_status()
                # Assuming the response has some success ID or we just return success
                return "hindsight-retained-id"
        except httpx.HTTPError as e:
            logger.error(f"Hindsight API request failed during retain: {e}. Falling back to local.")
            self.local_memory.append({"content": text, "metadata": metadata})
            return "local-id"
        except Exception as e:
            logger.error(f"Unexpected error during Hindsight retain: {e}. Falling back to local.")
            self.local_memory.append({"content": text, "metadata": metadata})
            return "local-id"

    async def search(self, query: str, limit: int = 5) -> list[MemoryRecord]:
        if not self.api_key or not self.bank_id:
            logger.warning("No Hindsight API key or bank ID configured, querying local fallback.")
            return self._local_search(query, limit)
            
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "query": query
                }
                response = await client.post(
                    f"{self.url}/v1/default/banks/{self.bank_id}/memories/recall",
                    json=payload,
                    headers=self.headers,
                    timeout=5.0
                )
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])
                
                # Map official Hindsight result.text to our MemoryRecord.content
                return [MemoryRecord(content=item.get("text", ""), metadata={"source": "hindsight"}) for item in results]
        except httpx.HTTPError as e:
            logger.error(f"Hindsight API request failed during recall: {e}. Using local fallback.")
            return self._local_search(query, limit)
        except Exception as e:
            logger.error(f"Unexpected error during Hindsight recall: {e}. Using local fallback.")
            return self._local_search(query, limit)

    def _local_search(self, query: str, limit: int) -> list[MemoryRecord]:
        results = []
        for mem in self.local_memory:
            if any(word.lower() in mem["content"].lower() for word in query.lower().split()):
                results.append(MemoryRecord(content=mem["content"], metadata=mem["metadata"]))
        return results[:limit]
