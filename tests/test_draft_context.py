from writersroom.agents.draft_context import DraftContextBuilder
from writersroom.domains.story.character import Character
from writersroom.domains.story.project import Project
from writersroom.draft.draft import Draft, DraftScene


class StubDraftService:
    def __init__(self, draft):
        self.draft = draft

    def current(self, path):
        return self.draft if path else None


def make_project() -> Project:
    project = Project("The Wine Game")
    project.draft_path = "draft.fountain"
    project.add_character(Character("Zoe"))
    project.add_character(Character("Marcus"))
    return project


DRAFT = Draft(
    scenes=[
        DraftScene(1, "INT. BAR - NIGHT", "Zoe drinks alone.", ["Zoe"]),
        DraftScene(2, "EXT. STREET - NIGHT", "Marcus follows Zoe.", ["Zoe", "Marcus"]),
        DraftScene(3, "INT. FLAT - DAY", "Zoe can't sleep.", ["Zoe"]),
    ]
)


def main():
    print("Testing DraftContextBuilder...")

    builder = DraftContextBuilder(StubDraftService(DRAFT))

    #
    # No draft linked
    #

    assert builder.build(Project("Empty"), "anything") == ""

    project = make_project()

    #
    # Focus by scene number
    #

    by_number = builder.build(project, "does scene 2 land?")
    assert "focus scene 2" in by_number
    assert "SCENE 2: EXT. STREET - NIGHT" in by_number
    assert "Marcus follows Zoe." in by_number
    assert "OUTLINE" in by_number
    assert "1. INT. BAR - NIGHT" in by_number

    #
    # Focus by character -> their most recent scene
    #

    by_character = builder.build(project, "how is Marcus doing here")
    assert "focus scene 2" in by_character

    #
    # Default with no signal: the last scene
    #

    default = builder.build(project, "general pacing thoughts")
    assert "focus scene 3 (last scene)" in default

    #
    # A detected edit wins over "last scene"
    #

    edited = Draft(
        scenes=list(DRAFT.scenes),
        changed_scenes=[2],
    )
    builder_edited = DraftContextBuilder(StubDraftService(edited))
    from_edit = builder_edited.build(project, "general pacing thoughts")
    assert "focus scene 2 (just edited)" in from_edit

    print()
    print(by_number)
    print()
    print("DraftContextBuilder tests passed.")


if __name__ == "__main__":
    main()
