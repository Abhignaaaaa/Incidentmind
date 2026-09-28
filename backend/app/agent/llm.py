class MockLLM:
    """Mock LLM for Phase 1."""
    def generate(self, prompt: str, context: str) -> str:
        if "Redis connection failures" in prompt and "pool exhaustion" in context:
            return "Based on past incidents, this looks like Redis connection pool exhaustion. Recommendation: Increase pool size and restart affected workers."
        elif "Redis connection failures" in prompt:
            return "I am seeing Redis connection failures, but I don't have past memory of this yet. You might want to check logs or runbooks."
        return f"I received your message: '{prompt}'. I will investigate."
