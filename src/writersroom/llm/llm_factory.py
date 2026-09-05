import os

from writersroom.llm.anthropic_client import AnthropicClient
from writersroom.llm.client import OllamaClient


def create_extraction_llm():
    """Create the language model client used for knowledge extraction."""

    provider = os.getenv(
        "WRITERSROOM_EXTRACTION_PROVIDER",
        "anthropic",
    ).lower()

    if provider == "ollama":
        return OllamaClient()

    model = os.getenv(
        "WRITERSROOM_ANTHROPIC_MODEL",
        "claude-sonnet-5",
    )

    return AnthropicClient(model=model)
