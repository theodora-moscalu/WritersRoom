from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.extraction.knowledge_record import (
    KnowledgeRecord,
)
from writersroom.extraction.knowledge_transformer import (
    KnowledgeTransformer,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():

    print(
        "Testing KnowledgeTransformer..."
    )

    transformer = (
        KnowledgeTransformer()
    )

    record = KnowledgeRecord(
        knowledge_level=(
            KnowledgeLevel.PRINCIPLE
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
            "This immediately establishes "
            "identity."
        ),
    )

    unit = SourceUnit(
        sequence=5,
        heading="INT. HOUSE",
        text="Scene text",
        unit_type=(
            SourceUnitType.SCENE
        ),
    )

    claim = transformer.transform(
        record,
        unit,
    )

    assert (
        claim.text
        == record.text
    )

    assert (
        claim.explanation
        == record.explanation
    )

    assert (
        claim.knowledge_level
        == KnowledgeLevel.PRINCIPLE
    )

    assert (
        claim.knowledge_domain
        == KnowledgeDomain.CHARACTER
    )

    assert (
        len(claim.provenance)
        == 1
    )

    assert (
        claim.provenance[0]
        .passage_sequence
        == 5
    )

    print(
        "KnowledgeTransformer tests passed."
    )


if __name__ == "__main__":
    main()