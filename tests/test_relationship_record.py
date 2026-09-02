from writersroom.domains.enums.knowledge_relationship_type import (
    KnowledgeRelationshipType,
)
from writersroom.relationship.relationship_record import (
    RelationshipRecord,
)


def main():

    print(
        "Testing RelationshipRecord..."
    )

    record = (
        RelationshipRecord(
            source_claim_id="1",
            target_claim_id="2",
            relationship_type=(
                KnowledgeRelationshipType.SIMILAR_TO
            ),
            confidence=0.94,
            reasoning=(
                "The claims express the same storytelling idea."
            ),
        )
    )

    assert (
        record.source_claim_id
        == "1"
    )

    assert (
        record.target_claim_id
        == "2"
    )

    assert (
        record.relationship_type
        == KnowledgeRelationshipType.SIMILAR_TO
    )

    assert (
        record.confidence
        == 0.94
    )

    assert (
        record.reasoning
        == (
            "The claims express the same storytelling idea."
        )
    )

    print()

    print(
        "RelationshipRecord tests passed."
    )


if __name__ == "__main__":
    main()