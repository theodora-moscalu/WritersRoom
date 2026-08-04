from abc import ABC

from writersroom.llm.client import OllamaClient


class Agent(ABC):
    """Base class for all WritersRoom agents."""

    def __init__(
        self,
        name: str,
        prompt_file: str,
    ):
        self.name = name

        self.llm = (
            OllamaClient()
        )

        self.system_prompt = (
            self.llm.load_prompt(
                prompt_file
            )
        )

    def ask_llm(
        self,
        messages: list[
            dict[str, str]
        ],
    ) -> str:
        """Send messages to the language model."""

        return self.llm.ask(
            messages
        )