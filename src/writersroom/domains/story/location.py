class Location:
    """Represents a story location."""

    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        """Convert the location to a dictionary."""

        return {
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Location from a dictionary."""

        return cls(
            data["name"],
        )

    def __str__(self):
        return self.name