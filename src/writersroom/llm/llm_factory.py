import os

from writersroom.llm.anthropic_client import AnthropicClient
from writersroom.llm.client import OllamaClient


def _create_llm(
    provider_var: str,
    model_var: str,
):
    """Create a language model client from a pair of environment variables."""

    provider = os.getenv(
        provider_var,
        "anthropic",
    ).lower()

    if provider == "ollama":
        return OllamaClient()

    model = os.getenv(
        model_var,
        "claude-sonnet-5",
    )

    return AnthropicClient(model=model)


def create_extraction_llm():
    """Create the language model client used for knowledge extraction."""

    return _create_llm(
        "WRITERSROOM_EXTRACTION_PROVIDER",
        "WRITERSROOM_ANTHROPIC_MODEL",
    )


def create_showrunner_llm():
    """Create the language model client used by the Showrunner."""

    return _create_llm(
        "WRITERSROOM_SHOWRUNNER_PROVIDER",
        "WRITERSROOM_SHOWRUNNER_MODEL",
    )
