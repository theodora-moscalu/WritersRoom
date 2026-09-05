from ollama import chat


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