from writersroom.domains.enums.relationship_type import (
    RelationshipType,
)
from writersroom.domains.story.character import Character
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.domains.story.project import Project
from writersroom.domains.story.relationship_beat import (
    RelationshipBeat,
)
from writersroom.graph.character_graph import CharacterGraph


def build_project() -> Project:
    project = Project("The Wine Game")

    for name in ("Nadia", "Marcus", "Zoe", "Elena"):
        project.add_character(Character(name))

    nadia_marcus = CharacterRelationship(
        source="Nadia",
        relationship=RelationshipType.RIVALS,
        target="Marcus",
        history=[
            RelationshipBeat(
                episode="1x04",
                description="the forgery is exposed",
                becomes="Rivals",
            )
        ],
    )
    project.add_character_relationship(nadia_marcus)
    project.add_character_relationship(
        CharacterRelationship("Marcus", RelationshipType.MANAGES, "Zoe")
    )

    return project


def main():
    print("Testing CharacterGraph...")

    graph = CharacterGraph.from_project(build_project())

    assert set(graph.characters()) == {"Nadia", "Marcus", "Zoe", "Elena"}

    assert graph.isolated() == ["Elena"]

    neighbours = graph.neighbours("Marcus")
    assert ("Zoe", "Manages", "->") in neighbours
    assert ("Nadia", "Rivals", "<-") in neighbours

    assert graph.path_between("Nadia", "Zoe") == ["Nadia", "Marcus", "Zoe"]
    assert graph.path_between("Nadia", "Elena") is None

    top = graph.most_connected(limit=1)
    assert top[0][0] == "Marcus"

    block = graph.render_block(["nadia"])
    assert "Nadia --Rivals--> Marcus" in block
    assert "the forgery is exposed" in block
    assert "Zoe" not in block  # not within Nadia's 1-hop ego graph

    dot = graph.to_dot()
    assert '"Nadia" -> "Marcus"' in dot
    assert "label=\"Rivals\"" in dot

    print()
    print(block)
    print()
    print("CharacterGraph tests passed.")


if __name__ == "__main__":
    main()
