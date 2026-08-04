from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.extraction.extraction import (
    Extraction,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


def main():
    print(
        "Testing Extraction..."
    )

    unit = SourceUnit(
        sequence=1,
        heading="INT. HOUSE - DAY",
        text="John enters.",
        unit_type=SourceUnitType.SCENE,
    )

    claim = ExtractedClaim(
        text="John is introduced.",
        knowledge_level=KnowledgeLevel.OBSERVATION,
        knowledge_domain=KnowledgeDomain.CHARACTER,
    )

    extraction = Extraction(
        source_unit=unit,
        agent="simple",
        claims=[claim],
    )

    assert (
        extraction.source_unit
        == unit
    )

    assert (
        extraction.agent
        == "simple"
    )

    assert (
        len(extraction.claims)
        == 1
    )

    print(
        "Extraction tests passed."
    )


if __name__ == "__main__":
    main()