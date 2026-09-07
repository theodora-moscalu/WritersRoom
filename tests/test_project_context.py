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
from writersroom.domains.story.episode import (
    Episode,
)
from writersroom.domains.story.note import (
    Note,
)
from writersroom.domains.story.project import (
    Project,
)
from writersroom.domains.story.season import (
    Season,
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
            want="recognition from the old guard",
            flaw="contempt for inherited status",
        )
    )

    season = Season(
        number=1,
        title="Foundations",
        question="Will the old guard ever accept Zoe?",
        arc="Outsider to insider to exposed.",
    )
    project.add_season(season)
    project.add_episode(Episode("Pilot", logline="Zoe arrives."))
    season.add_episode_title("Pilot")

    from writersroom.domains.story.relationship_beat import RelationshipBeat

    project.add_character_relationship(
        CharacterRelationship(
            source="Zoe",
            relationship=RelationshipType.RIVALS,
            target="Marcus",
            history=[
                RelationshipBeat(
                    episode="1x04",
                    description="Marcus exposes Zoe's forgery",
                    becomes="Rivals",
                )
            ],
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
    assert "want: recognition from the old guard" in block
    assert "flaw: contempt for inherited status" in block
    assert "Season 1: Foundations" in block
    assert "question: Will the old guard ever accept Zoe?" in block
    assert "- Pilot" in block
    assert "1x04" in block  # relationship history tail
    assert "Marcus exposes Zoe's forgery" in block

    print()
    print(block)
    print()

    print("ProjectContextBuilder tests passed.")


if __name__ == "__main__":
    main()
