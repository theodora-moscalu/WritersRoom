from dataclasses import dataclass
from dataclasses import field

from writersroom.relationship.relationship_proposal import (
    RelationshipProposal,
)


@dataclass
class RelationshipDiscoveryResult:
    """Relationships proposed during discovery."""

    proposals: list[
        RelationshipProposal
    ] = field(
        default_factory=list
    )

    metadata: dict[
        str,
        str,
    ] = field(
        default_factory=dict
    )