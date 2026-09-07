from writersroom.agents.graph_context import GraphContextBuilder
from writersroom.domains.enums.relationship_type import (
    RelationshipType,
)
from writersroom.domains.story.character import Character
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.domains.story.project import Project


def main():
    print("Testing GraphContextBuilder...")

    builder = GraphContextBuilder(whole_graph_limit=8)

    #
    # Empty project -> empty block
    #

    assert builder.build(Project("Empty"), "anything") == ""

    project = Project("The Wine Game")
    for name in ("Nadia", "Marcus", "Zoe"):
        project.add_character(Character(name))
    project.add_character_relationship(
        CharacterRelationship("Nadia", RelationshipType.MENTORS, "Marcus")
    )
    project.add_character_relationship(
        CharacterRelationship("Marcus", RelationshipType.MANAGES, "Zoe")
    )

    #
    # Focus named -> ego block for that character
    #

    focused = builder.build(
        project,
        "How should the scene with Nadia land?",
    )
    assert "Nadia --Mentors--> Marcus" in focused
    assert "Marcus --Manages--> Zoe" not in focused  # outside Nadia's ego

    #
    # No focus + small graph -> whole web
    #

    whole = builder.build(project, "general pacing question")
    assert "Nadia --Mentors--> Marcus" in whole
    assert "Marcus --Manages--> Zoe" in whole

    #
    # No focus + large graph -> empty (ProjectContextBuilder still lists the cast)
    #

    for i in range(12):
        project.add_character(Character(f"Extra {i}"))

    assert builder.build(project, "general pacing question") == ""

    print()
    print(focused)
    print()
    print("GraphContextBuilder tests passed.")


if __name__ == "__main__":
    main()
