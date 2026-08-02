class Scene:
    """Represents a single scene within an episode."""

    def __init__(
        self,
        number: int,
        heading: str = "",
        summary: str = "",
        characters: list[str] | None = None,
        locations: list[str] | None = None,
    ):
        self.number = number
        self.heading = heading
        self.summary = summary
        self.characters = characters or []
        self.locations = locations or []

    def to_dict(self):
        """Convert the scene to a dictionary."""

        return {
            "number": self.number,
            "heading": self.heading,
            "summary": self.summary,
            "characters": self.characters,
            "locations": self.locations,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Scene from a dictionary."""

        return cls(
            number=data["number"],
            heading=data.get("heading", ""),
            summary=data.get("summary", ""),
            characters=data.get("characters", []),
            locations=data.get("locations", []),
        )

    def __str__(self):
        if self.heading:
            return f"Scene {self.number}: {self.heading}"

        return f"Scene {self.number}"