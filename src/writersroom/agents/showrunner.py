from writersroom.agents.base_agent import (
    Agent,
)
from writersroom.domains.story.project import (
    Project,
)


class Showrunner(Agent):
    """AI agent responsible for guiding the writing process."""

    def __init__(
        self,
        project: Project,
    ):
        super().__init__(
            name="Showrunner",
            prompt_file="showrunner.txt",
        )

        self.project = project

    def respond(
        self,
        prompt: str,
    ) -> str:
        """Generate a response from the Showrunner."""

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        messages.extend(
            self.project.conversation_history
        )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.ask_llm(
            messages
        )

        self.project.conversation_history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        self.project.conversation_history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response