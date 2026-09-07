from writersroom.domains.enums.relationship_type import RelationshipType
from writersroom.domains.story.relationship_beat import RelationshipBeat


class CharacterRelationship:
    """Represents a relationship between two characters."""

    def __init__(
        self,
        source: str,
        relationship: RelationshipType,
        target: str,
        history: list[RelationshipBeat] | None = None,
    ):
        self.source = source
        self.relationship = relationship
        self.target = target
        self.history = history or []

    def add_beat(self, beat: RelationshipBeat):
        """Record a shift in the relationship."""

        self.history.append(beat)

    def to_dict(self):
        """Convert the relationship to a dictionary."""

        return {
            "source": self.source,
            "relationship": self.relationship.value,
            "target": self.target,
            "history": [
                beat.to_dict()
                for beat in self.history
            ],
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
            history=[
                RelationshipBeat.from_dict(beat)
                for beat in data.get("history", [])
            ],
        )

    def __str__(self):
        line = (
            f"{self.source} "
            f"--{self.relationship.value}--> "
            f"{self.target}"
        )

        if self.history:
            line += "  (" + "; ".join(
                str(beat) for beat in self.history
            ) + ")"

        return line
