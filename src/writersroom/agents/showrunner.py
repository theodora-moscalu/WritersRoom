from writersroom.domains.story.project import Project
from writersroom.llm.client import OllamaClient


class Showrunner:
    """AI agent responsible for guiding the writing process."""

    def __init__(self, project: Project):
        self.name = "Showrunner"
        self.project = project
        self.client = OllamaClient()
        self.system_prompt = self.client.load_prompt("showrunner.txt")

    def respond(self, prompt: str) -> str:
        """Generate a response from the Showrunner agent."""

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        messages.extend(self.project.conversation_history)

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.ask(messages)

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