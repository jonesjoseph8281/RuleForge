from app.llm.base import LLMProvider
from app.llm.providers.mock_provider import MockProvider

def get_provider(provider_name: str) -> LLMProvider:
    if provider_name == "mock":
        return MockProvider()
    # Others would be instantiated here
    raise ValueError(f"Unknown provider {provider_name}")
