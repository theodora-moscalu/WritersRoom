from writersroom.domains.entity import Entity


class Character(Entity):
    """Represents a character in the project."""

    def __init__(
        self,
        name: str,
        description: str = "",
        traits: list[str] | None = None,
        want: str = "",
        need: str = "",
        flaw: str = "",
        arc: str = "",
        backstory: str = "",
        voice: str = "",
    ):
        self.name = name
        self.description = description
        self.traits = traits or []
        self.want = want
        self.need = need
        self.flaw = flaw
        self.arc = arc
        self.backstory = backstory
        self.voice = voice

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
            "traits": self.traits,
            "want": self.want,
            "need": self.need,
            "flaw": self.flaw,
            "arc": self.arc,
            "backstory": self.backstory,
            "voice": self.voice,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Character from a dictionary."""

        return cls(
            name=data["name"],
            description=data.get("description", ""),
            traits=data.get("traits", []),
            want=data.get("want", ""),
            need=data.get("need", ""),
            flaw=data.get("flaw", ""),
            arc=data.get("arc", ""),
            backstory=data.get("backstory", ""),
            voice=data.get("voice", ""),
        )

    def __str__(self):
        return self.display_name
