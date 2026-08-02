from writersroom.domains.entity import Entity


class Character(Entity):
    """Represents a character in the project."""

    def __init__(
        self,
        name: str,
        description: str = "",
    ):
        self.name = name
        self.description = description

    @property
    def identity(self) -> str:
        """Return the character's stable identity."""

        return self.name

    @property
    def display_name(self) -> str:
        """Return the character's display name."""

        return self.name

    def to_dict(self):
        """Convert the character to a dictionary."""

        return {
            "name": self.name,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Character from a dictionary."""

        return cls(
            name=data["name"],
            description=data.get(
                "description",
                "",
            ),
        )

    def __str__(self):
        return self.display_name