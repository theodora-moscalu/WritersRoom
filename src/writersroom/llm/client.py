from ollama import chat

from writersroom.llm.json_parsing import (
    parse_json_object,
)


class OllamaClient:
    """Simple wrapper around the local Ollama server."""

    def __init__(self, model: str = "qwen3:8b"):
        self.model = model

    def ask(self, messages: list[dict]) -> str:
        """Send a list of chat messages to the language model."""

        response = chat(
            model=self.model,
            messages=messages,
        )

        return response.message.content

    def respond_json(self, messages: list[dict]) -> dict:
        """Ask for a JSON object and return it parsed (best effort)."""

        return parse_json_object(self.ask(messages))