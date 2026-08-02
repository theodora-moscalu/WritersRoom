from enum import Enum


class EpisodeStatus(Enum):
    """Represents the writing status of an episode."""

    OUTLINE = "Outline"
    FIRST_DRAFT = "First Draft"
    REVISED = "Revised"
    FINAL = "Final"

    def __str__(self) -> str:
        return self.value