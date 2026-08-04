from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.extraction.knowledge_record import (
    KnowledgeRecord,
)


def main():

    print(
        "Testing KnowledgeRecord..."
    )

    record = KnowledgeRecord(
        knowledge_level=(
            KnowledgeLevel.OBSERVATION
        ),
        knowledge_domain=(
            KnowledgeDomain.CHARACTER
        ),
        importance="HIGH",
        text=(
            "Introduce the protagonist "
            "performing their defining skill."
        ),
        explanation=(
            "Showing competence immediately "
            "establishes identity."
        ),
    )

    assert (
        record.knowledge_level
        == KnowledgeLevel.OBSERVATION
    )

    assert (
        record.knowledge_domain
        == KnowledgeDomain.CHARACTER
    )

    assert (
        record.importance
        == "HIGH"
    )

    assert (
        record.text
        == (
            "Introduce the protagonist "
            "performing their defining skill."
        )
    )

    assert (
        record.explanation
        == (
            "Showing competence immediately "
            "establishes identity."
        )
    )

    print(
        "KnowledgeRecord tests passed."
    )


if __name__ == "__main__":
    main()