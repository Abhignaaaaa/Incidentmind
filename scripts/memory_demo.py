import asyncio
import sys
import os

# Adjust path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.memory.service import memory_service
from app.agent.llm import MockLLM

async def run_demo():
    print("=== INCIDENTMIND MEMORY DEMO ===")
    llm = MockLLM()
    
    print("\n--- SCENARIO 1: WITHOUT MEMORY ---")
    query = "Redis connection failures are happening again"
    print(f"User: {query}")
    
    memories = await memory_service.recall(query)
    context = ""
    if memories:
        context = "Memory:\n" + "\n".join([m.content for m in memories])
    
    response = llm.generate(query, context)
    print(f"Agent Response: {response}")
    print(f"Memory Used: {len(memories) > 0}")
    
    print("\n--- LEARNING PHASE ---")
    learning = "Root cause: Redis connection pool exhaustion. Resolution: Increase connection pool size and restart affected workers."
    print(f"System learns: {learning}")
    await memory_service.retain(learning)
    print("Learning retained via Hindsight service.")
    
    print("\n--- SCENARIO 2: WITH HINDSIGHT MEMORY ---")
    print(f"User: {query}")
    
    memories_2 = await memory_service.recall(query)
    context_2 = ""
    if memories_2:
        context_2 = "Memory:\n" + "\n".join([m.content for m in memories_2])
        
    response_2 = llm.generate(query, context_2)
    print(f"Agent Response: {response_2}")
    print(f"Memory Used: {len(memories_2) > 0}")

if __name__ == "__main__":
    asyncio.run(run_demo())
