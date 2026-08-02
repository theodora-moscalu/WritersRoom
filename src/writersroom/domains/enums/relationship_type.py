from enum import Enum


class RelationshipType(Enum):
    """The type of relationship between two characters."""

    ALLY = "Ally"
    ENEMY = "Enemy"
    FRIEND = "Friend"
    FAMILY = "Family"
    LOVES = "Loves"
    REPORTS_TO = "Reports To"
    MANAGES = "Manages"
    MENTORS = "Mentors"
    RIVALS = "Rivals"
    TRUSTS = "Trusts"

    def __str__(self):
        return self.value