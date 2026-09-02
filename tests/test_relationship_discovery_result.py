from writersroom.domains.enums.knowledge_relationship_type import (
    KnowledgeRelationshipType,
)
from writersroom.relationship.relationship_discovery_result import (
    RelationshipDiscoveryResult,
)
from writersroom.relationship.relationship_proposal import (
    RelationshipProposal,
)


def main():

    print(
        "Testing RelationshipDiscoveryResult..."
    )

    proposal = (
        RelationshipProposal(
            source_claim_id="claim-1",
            target_claim_id="claim-2",
            relationship_type=(
                KnowledgeRelationshipType.SUPPORTS
            ),
            confidence=0.95,
            reasoning=(
                "Both claims express "
                "compatible storytelling advice."
            ),
        )
    )

    result = (
        RelationshipDiscoveryResult(
            proposals=[
                proposal
            ],
            metadata={
                "discoverer": (
                    "relationship_service"
                ),
            },
        )
    )

    assert (
        len(
            result.proposals
        )
        == 1
    )

    assert (
        result.proposals[0]
        == proposal
    )

    assert (
        result.metadata[
            "discoverer"
        ]
        == "relationship_service"
    )

    print()

    print(
        "RelationshipDiscoveryResult tests passed."
    )


if __name__ == "__main__":
    main()