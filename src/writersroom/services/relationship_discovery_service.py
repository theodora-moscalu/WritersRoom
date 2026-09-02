from writersroom.agents.relationship_analyser import (
    RelationshipAnalyser,
)
from writersroom.relationship.relationship_discovery_result import (
    RelationshipDiscoveryResult,
)
from writersroom.relationship.relationship_proposal import (
    RelationshipProposal,
)


class RelationshipDiscoveryService:
    """Coordinates relationship discovery."""

    def __init__(
        self,
        analyser: RelationshipAnalyser | None = None,
    ):
        self.analyser = (
            analyser
            or RelationshipAnalyser()
        )

    def discover(
        self,
        claim_a,
        claim_b,
    ) -> RelationshipDiscoveryResult:
        """Discover relationships between two claims."""

        records = (
            self.analyser.analyse(
                claim_a,
                claim_b,
            )
        )

        proposals = [
            RelationshipProposal(
                source_claim_id=(
                    record.source_claim_id
                ),
                target_claim_id=(
                    record.target_claim_id
                ),
                relationship_type=(
                    record.relationship_type
                ),
                confidence=(
                    record.confidence
                ),
                reasoning=(
                    record.reasoning
                ),
            )
            for record in records
        ]

        return (
            RelationshipDiscoveryResult(
                proposals=proposals,
                metadata={
                    "analyser": (
                        "relationship_analyser"
                    ),
                },
            )
        )