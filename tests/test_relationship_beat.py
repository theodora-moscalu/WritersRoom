from writersroom.domains.enums.relationship_type import (
    RelationshipType,
)
from writersroom.domains.story.character_relationship import (
    CharacterRelationship,
)
from writersroom.domains.story.relationship_beat import (
    RelationshipBeat,
)


def main():
    print("Testing RelationshipBeat...")

    relationship = CharacterRelationship(
        source="Nadia",
        relationship=RelationshipType.MENTORS,
        target="Marcus",
    )

    relationship.add_beat(
        RelationshipBeat(
            episode="1x04",
            description="Nadia learns Marcus forged the provenance",
            becomes="Rivals",
        )
    )

    reloaded = CharacterRelationship.from_dict(
        relationship.to_dict()
    )

    assert reloaded.relationship == RelationshipType.MENTORS
    assert len(reloaded.history) == 1

    beat = reloaded.history[0]
    assert beat.episode == "1x04"
    assert beat.becomes == "Rivals"
    assert "forged the provenance" in beat.description

    #
    # An old blob with no history still loads
    #

    legacy = CharacterRelationship.from_dict(
        {
            "source": "Zoe",
            "relationship": "Ally",
            "target": "Nadia",
        }
    )
    assert legacy.history == []

    print()
    print(reloaded)
    print()
    print("RelationshipBeat tests passed.")


if __name__ == "__main__":
    main()
