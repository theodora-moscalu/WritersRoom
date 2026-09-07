from writersroom.agents.project_context import (
    ProjectContextBuilder,
)
from writersroom.agents.showrunner import (
    Showrunner,
)
from writersroom.domains.story.character import (
    Character,
)
from writersroom.domains.story.project import (
    Project,
)


class RecordingClient:
    """Captures the messages it is asked to answer."""

    def __init__(self):
        self.last_messages = None

    def ask(self, messages):
        self.last_messages = messages

        return "Open on her alone. Grounded in: [CL000042]"


class StubKnowledgeContext:
    def __init__(self):
        self.last_query = None
        self.last_context = None

    def build(self, query_text, context_text=""):
        self.last_query = query_text
        self.last_context = context_text
        return "RELEVANT KNOWLEDGE FROM THE LIBRARY\n[CL000042] ..."


class StubGraphContext:
    def build(self, project, focus_text):
        return "CHARACTER GRAPH\n  Zoe --Rivals--> Marcus"


class StubDraftContext:
    _SCENE_TEXT = "Zoe faces Marcus across the cellar. The forgery is between them."

    def build(self, project, focus_text):
        return (
            "CURRENT DRAFT — 3 scenes, focus scene 3 (just edited)\n\n"
            f"SCENE 3: INT. CELLAR\n{self._SCENE_TEXT}"
        )

    def focus_scene(self, project, focus_text):
        class _Scene:
            text = StubDraftContext._SCENE_TEXT

        return _Scene()


def main():
    print("Testing Showrunner...")

    project = Project("The Wine Game")
    project.add_character(
        Character(name="Zoe", description="A sommelier.")
    )

    client = RecordingClient()
    knowledge = StubKnowledgeContext()

    showrunner = Showrunner(
        project,
        llm=client,
        knowledge_context=knowledge,
        project_context=ProjectContextBuilder(),
        graph_context=StubGraphContext(),
        draft_context=StubDraftContext(),
    )

    reply = showrunner.respond(
        "How should I introduce Zoe?"
    )

    system = client.last_messages[0]

    assert system["role"] == "system"
    assert "You are Showrunner" in system["content"]
    assert "CURRENT PROJECT: The Wine Game" in system["content"]
    assert "RELEVANT KNOWLEDGE FROM THE LIBRARY" in system["content"]
    assert "CHARACTER GRAPH" in system["content"]
    assert "CURRENT DRAFT" in system["content"]

    #
    # The library search is steered by the focus scene, not just the message
    #

    assert knowledge.last_query == "How should I introduce Zoe?"
    assert "forgery is between them" in knowledge.last_context

    #
    # The user turn is the last message
    #

    assert client.last_messages[-1] == {
        "role": "user",
        "content": "How should I introduce Zoe?",
    }

    #
    # History holds the plain turns, not the injected context
    #

    assert project.conversation_history == [
        {
            "role": "user",
            "content": "How should I introduce Zoe?",
        },
        {
            "role": "assistant",
            "content": reply,
        },
    ]

    #
    # A second turn replays history but not stale knowledge
    #

    showrunner.respond("What about the pacing?")

    replayed = client.last_messages

    assert replayed[1]["content"] == "How should I introduce Zoe?"
    assert all(
        message["role"] != "system"
        for message in replayed[1:]
    )

    print()
    print("Showrunner tests passed.")


if __name__ == "__main__":
    main()
