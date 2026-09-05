from writersroom.agents.project_context import (
    ProjectContextBuilder,
)
from writersroom.domains.enums.note_target_type import (
    NoteTargetType,
)
from writersroom.domains.enums.relationship_type import (
    RelationshipType,
)
from writersroom.domains.story.character import (
    Character,
)
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.domains.story.note import (
    Note,
)
from writersroom.domains.story.project import (
    Project,
)


def main():
    print("Testing ProjectContextBuilder...")

    builder = ProjectContextBuilder()

    assert builder.build(Project("Empty")) == ""

    project = Project("The Wine Game")

    project.add_character(
        Character(
            name="Zoe",
            description="A sommelier hiding a fraud.",
        )
    )

    project.add_character_relationship(
        CharacterRelationship(
            source="Zoe",
            relationship=RelationshipType.RIVALS,
            target="Marcus",
        )
    )

    project.add_note(
        Note(
            title="Audience trust",
            target_type=NoteTargetType.PROJECT,
            target_id=project.title,
            content=(
                "The audience should distrust Zoe until episode 4."
            ),
        )
    )

    block = builder.build(project)

    assert "CURRENT PROJECT: The Wine Game" in block
    assert "Zoe" in block
    assert "sommelier hiding a fraud" in block
    assert "Marcus" in block
    assert "distrust Zoe until episode 4" in block

    print()
    print(block)
    print()

    print("ProjectContextBuilder tests passed.")


if __name__ == "__main__":
    main()
