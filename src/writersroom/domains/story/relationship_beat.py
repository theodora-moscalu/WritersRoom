class RelationshipBeat:
    """A moment when a relationship shifts."""

    def __init__(
        self,
        episode: str = "",
        description: str = "",
        becomes: str = "",
    ):
        self.episode = episode
        self.description = description
        self.becomes = becomes

    def to_dict(self):
        """Convert the beat to a dictionary."""

        return {
            "episode": self.episode,
            "description": self.description,
            "becomes": self.becomes,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a RelationshipBeat from a dictionary."""

        return cls(
            episode=data.get("episode", ""),
            description=data.get("description", ""),
            becomes=data.get("becomes", ""),
        )

    def __str__(self):
        prefix = f"{self.episode}: " if self.episode else ""

        if self.becomes:
            return f"{prefix}becomes {self.becomes}" + (
                f" ({self.description})" if self.description else ""
            )

        return f"{prefix}{self.description}".strip(": ")
