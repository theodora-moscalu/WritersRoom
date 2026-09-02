from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.services.relationship_discovery_service import (
    RelationshipDiscoveryService,
)


def main():

    print(
        "Testing RelationshipDiscoveryService..."
    )

    service = (
        RelationshipDiscoveryService()
    )

    claim_a = Claim(
        identity="claim-1",
        passage_id="passage-1",
        text=(
            "Conflict escalates tension."
        ),
        knowledge_level=(
            KnowledgeLevel.PRINCIPLE
        ),
        knowledge_domain=(
            KnowledgeDomain.CONFLICT
        ),
    )

    claim_b = Claim(
        identity="claim-2",
        passage_id="passage-2",
        text=(
            "Increasing obstacles raise dramatic stakes."
        ),
        knowledge_level=(
            KnowledgeLevel.PRINCIPLE
        ),
        knowledge_domain=(
            KnowledgeDomain.CONFLICT
        ),
    )

    result = (
        service.discover(
            claim_a,
            claim_b,
        )
    )

    assert (
        len(
            result.proposals
        )
        == 0
    )

    assert (
        result.metadata[
            "analyser"
        ]
        == "relationship_analyser"
    )

    print()

    print(
        "RelationshipDiscoveryService tests passed."
    )


if __name__ == "__main__":
    main()