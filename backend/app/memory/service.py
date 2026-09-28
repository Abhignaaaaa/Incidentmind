from .hindsight import HindsightClient
from .schemas import MemoryRecord
from typing import List

class MemoryService:
    def __init__(self):
        self.client = HindsightClient()

    async def retain(self, content: str, metadata: dict = None) -> str:
        metadata = metadata or {}
        return await self.client.store(content, metadata)

    async def recall(self, query: str, limit: int = 5) -> List[MemoryRecord]:
        return await self.client.search(query, limit)

memory_service = MemoryService()
