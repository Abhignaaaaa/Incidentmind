from sqlalchemy.orm import Session
from app.memory.service import memory_service
from app.agent.llm import MockLLM
from app.agent.tools import search_incidents

class Agent:
    def __init__(self, db: Session):
        self.db = db
        self.llm = MockLLM()

    async def process_message(self, message: str) -> dict:
        # 1. Recall memory
        memories = await memory_service.recall(message)
        memory_used = len(memories) > 0
        
        # 2. Search tools (read-only)
        db_results = search_incidents(self.db, message)
        
        # 3. Generate context
        context = ""
        sources = []
        if memory_used:
            context += "Memory:\n" + "\n".join([m.content for m in memories])
            sources.append("Hindsight Memory")
        if db_results:
            context += "\nIncidents:\n" + str(db_results)
            sources.append("Database Incidents")
            
        # 4. Generate response
        response = self.llm.generate(message, context)
        
        # 5. Retain learning (simplified for demo: if user gives us resolution info, we retain it)
        if "Root cause:" in message:
            await memory_service.retain(message, metadata={"source": "user_input"})
            
        return {
            "response": response,
            "memory_used": memory_used,
            "sources": sources
        }
