from enum import StrEnum


class KnowledgeDomain(StrEnum):
    """Domains of storytelling knowledge."""

    UNKNOWN = (
        "unknown"
    )

    STRUCTURE = (
        "structure"
    )

    CHARACTER = (
        "character"
    )

    SCENE = (
        "scene"
    )

    CONFLICT = (
        "conflict"
    )

    DIALOGUE = (
        "dialogue"
    )

    EMOTION = (
        "emotion"
    )

    THEME = (
        "theme"
    )

    VISUAL = (
        "visual"
    )

    WORLD = (
        "world"
    )

    WRITING = (
        "writing"
    )