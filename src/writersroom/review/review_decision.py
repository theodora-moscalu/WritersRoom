from enum import StrEnum


class ReviewDecision(StrEnum):
    """Possible review decisions."""

    ACCEPT = "accept"

    REJECT = "reject"

    EDIT = "edit"