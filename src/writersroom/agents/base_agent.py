from abc import ABC
from pathlib import Path

from writersroom.llm.client import OllamaClient


class Agent(ABC):
    """Base class for all WritersRoom agents."""

    def __init__(
        self,
        name: str,
        prompt_file: str,
        llm=None,
    ):
        self.name = name

        self.llm = (
            llm
            or OllamaClient()
        )

        self.system_prompt = (
            self.load_prompt(
                prompt_file
            )
        )

    @staticmethod
    def load_prompt(filename: str) -> str:
        prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
            / filename
        )

        return prompt_path.read_text(encoding="utf-8")

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