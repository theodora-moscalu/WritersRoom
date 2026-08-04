from enum import StrEnum


class ClaimCategory(StrEnum):
    """Categories of extracted claims."""

    STORY_PRINCIPLE = (
        "story_principle"
    )

    STRUCTURE = (
        "structure"
    )

    SCENE_PURPOSE = (
        "scene_purpose"
    )

    CHARACTER = (
        "character"
    )

    DIALOGUE = (
        "dialogue"
    )

    CONFLICT = (
        "conflict"
    )

    PACING = (
        "pacing"
    )

    WRITING_TECHNIQUE = (
        "writing_technique"
    )