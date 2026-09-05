import anthropic


class AnthropicClient:
    """Wrapper around the Anthropic Messages API, matching OllamaClient's interface."""

    def __init__(
        self,
        model: str = "claude-sonnet-5",
        max_tokens: int = 16000,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self._client = anthropic.Anthropic()

        if not (self._client.api_key or self._client.auth_token):
            raise RuntimeError(
                "No Anthropic credentials found. Set ANTHROPIC_API_KEY "
                "in your environment or .env file."
            )

    def ask(self, messages: list[dict]) -> str:
        """Send a list of chat messages to the language model."""

        system = "\n\n".join(
            message["content"]
            for message in messages
            if message["role"] == "system"
        )

        chat_messages = [
            message
            for message in messages
            if message["role"] != "system"
        ]

        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system or anthropic.NOT_GIVEN,
                messages=chat_messages,
                thinking={"type": "adaptive"},
            )
        except anthropic.AuthenticationError as error:
            raise RuntimeError(
                "Anthropic authentication failed. Set ANTHROPIC_API_KEY "
                "in your environment or .env file."
            ) from error

        return "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )
