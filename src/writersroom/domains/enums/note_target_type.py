from enum import Enum


class NoteTargetType(Enum):
    """The type of entity a note belongs to."""

    PROJECT = "Project"
    CHARACTER = "Character"
    LOCATION = "Location"
    EPISODE = "Episode"
    SCENE = "Scene"
    RELATIONSHIP = "Relationship"

    def __str__(self):
        return self.value