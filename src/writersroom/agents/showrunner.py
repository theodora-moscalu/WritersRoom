from writersroom.agents.base_agent import (
    Agent,
)
from writersroom.domains.story.project import (
    Project,
)
from writersroom.llm.llm_factory import (
    create_showrunner_llm,
)


class Showrunner(Agent):
    """AI agent responsible for guiding the writing process."""

    def __init__(
        self,
        project: Project,
        llm=None,
        knowledge_context=None,
        project_context=None,
    ):
        super().__init__(
            name="Showrunner",
            prompt_file="showrunner.txt",
            llm=llm or create_showrunner_llm(),
        )

        self.project = project
        self.knowledge_context = knowledge_context
        self.project_context = project_context

    def respond(
        self,
        prompt: str,
    ) -> str:
        """Generate a grounded response from the Showrunner."""

        knowledge_block = (
            self.knowledge_context.build(prompt)
            if self.knowledge_context
            else ""
        )

        project_block = (
            self.project_context.build(self.project)
            if self.project_context
            else ""
        )

        system = "\n\n".join(
            part
            for part in [
                self.system_prompt,
                project_block,
                knowledge_block,
            ]
            if part
        )

        messages = [
            {
                "role": "system",
                "content": system,
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
