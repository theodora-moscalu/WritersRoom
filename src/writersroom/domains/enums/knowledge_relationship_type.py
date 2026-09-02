from enum import Enum


class KnowledgeRelationshipType(
    Enum
):
    """The semantic relationship between two knowledge claims."""

    SIMILAR_TO = (
        "Similar To"
    )

    SUPPORTS = (
        "Supports"
    )

    CONTRADICTS = (
        "Contradicts"
    )

    def __str__(
        self,
    ):
        return self.value