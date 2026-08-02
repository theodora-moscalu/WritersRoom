from writersroom.domains.entity import Entity
from writersroom.domains.enums.episode_status import EpisodeStatus
from writersroom.domains.story.scene import Scene


class Episode(Entity):
    """Represents a television episode."""

    def __init__(
        self,
        title: str,
        logline: str = "",
        synopsis: str = "",
        status: EpisodeStatus = EpisodeStatus.OUTLINE,
        characters: list[str] | None = None,
        locations: list[str] | None = None,
        scenes: list[Scene] | None = None,
    ):
        self.title = title
        self.logline = logline
        self.synopsis = synopsis
        self.status = status
        self.characters = characters or []
        self.locations = locations or []
        self.scenes = scenes or []

    @property
    def identity(self) -> str:
        """Return the episode's stable identity."""

        return self.title

    @property
    def display_name(self) -> str:
        """Return the episode's display name."""

        return self.title

    def to_dict(self):
        """Convert the episode to a dictionary."""

        return {
            "title": self.title,
            "logline": self.logline,
            "synopsis": self.synopsis,
            "status": self.status.value,
            "characters": self.characters,
            "locations": self.locations,
            "scenes": [
                scene.to_dict()
                for scene in self.scenes
            ],
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Episode from a dictionary."""

        status = EpisodeStatus.OUTLINE

        if "status" in data:
            status = EpisodeStatus(data["status"])

        scenes = [
            Scene.from_dict(scene)
            for scene in data.get("scenes", [])
        ]

        return cls(
            title=data["title"],
            logline=data.get("logline", ""),
            synopsis=data.get("synopsis", ""),
            status=status,
            characters=data.get("characters", []),
            locations=data.get("locations", []),
            scenes=scenes,
        )

    def __str__(self):
        return self.display_name