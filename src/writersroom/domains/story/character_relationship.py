from writersroom.domains.enums.relationship_type import RelationshipType


class CharacterRelationship:
    """Represents a relationship between two characters."""

    def __init__(
        self,
        source: str,
        relationship: RelationshipType,
        target: str,
    ):
        self.source = source
        self.relationship = relationship
        self.target = target

    def to_dict(self):
        """Convert the relationship to a dictionary."""

        return {
            "source": self.source,
            "relationship": self.relationship.value,
            "target": self.target,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a relationship from a dictionary."""

        return cls(
            source=data["source"],
            relationship=RelationshipType(
                data["relationship"]
            ),
            target=data["target"],
        )

    def __str__(self):
        return (
            f"{self.source} "
            f"--{self.relationship.value}--> "
            f"{self.target}"
        )