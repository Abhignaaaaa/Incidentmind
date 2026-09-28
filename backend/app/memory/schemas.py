from pydantic import BaseModel
from typing import Optional, Dict, Any

class MemoryRecord(BaseModel):
    id: Optional[str] = None
    content: str
    metadata: Dict[str, Any] = {}
