from writersroom.domains.enums.knowledge_relationship_type import (
    KnowledgeRelationshipType,
)
from writersroom.relationship.relationship_proposal import (
    RelationshipProposal,
)


def main():

    print(
        "Testing RelationshipProposal..."
    )

    proposal = (
        RelationshipProposal(
            source_claim_id="claim-1",
            target_claim_id="claim-2",
            relationship_type=(
                KnowledgeRelationshipType.SIMILAR_TO
            ),
            confidence=0.91,
            reasoning=(
                "Both claims describe "
                "the same storytelling principle."
            ),
        )
    )

    assert (
        proposal.source_claim_id
        == "claim-1"
    )

    assert (
        proposal.target_claim_id
        == "claim-2"
    )

    assert (
        proposal.relationship_type
        == KnowledgeRelationshipType.SIMILAR_TO
    )

    assert (
        proposal.confidence
        == 0.91
    )

    assert (
        proposal.reasoning
        == (
            "Both claims describe "
            "the same storytelling principle."
        )
    )

    print()

    print(
        "RelationshipProposal tests passed."
    )


if __name__ == "__main__":
    main()