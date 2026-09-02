from writersroom.domains.enums.knowledge_relationship_type import (
    KnowledgeRelationshipType,
)
from writersroom.domains.knowledge.knowledge_relationship import (
    KnowledgeRelationship,
)


def main():

    print(
        "Testing KnowledgeRelationship..."
    )

    relationship = (
        KnowledgeRelationship(
            source_claim_id="claim-1",
            target_claim_id="claim-2",
            relationship_type=(
                KnowledgeRelationshipType.SUPPORTS
            ),
            confidence=0.92,
        )
    )

    assert (
        relationship.source_claim_id
        == "claim-1"
    )

    assert (
        relationship.target_claim_id
        == "claim-2"
    )

    assert (
        relationship.relationship_type
        == KnowledgeRelationshipType.SUPPORTS
    )

    assert (
        relationship.confidence
        == 0.92
    )

    print()

    print(
        "KnowledgeRelationship tests passed."
    )


if __name__ == "__main__":
    main()