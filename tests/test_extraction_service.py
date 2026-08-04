from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)
from writersroom.services.extraction_service import (
    ExtractionService,
)


def main():
    print(
        "Testing ExtractionService..."
    )

    service = (
        ExtractionService()
    )

    unit = SourceUnit(
        sequence=1,
        text=(
            "Conflict creates drama."
        ),
        unit_type=(
            SourceUnitType.PARAGRAPH
        ),
    )

    result = service.extract(
        unit
    )

    assert (
        len(result.claims)
        >= 1
    )

    claim = result.claims[0]

    assert (
        claim.text
        != ""
    )

    assert (
        claim.explanation
        != ""
    )

    assert (
        isinstance(
            claim.knowledge_level,
            KnowledgeLevel,
        )
    )

    assert (
        isinstance(
            claim.knowledge_domain,
            KnowledgeDomain,
        )
    )

    assert (
        len(claim.provenance)
        == 1
    )

    assert (
        claim.provenance[0]
        .passage_sequence
        == 1
    )

    assert (
        claim.provenance[0]
        .confidence
        == 1.0
    )

    assert (
        result.metadata[
            "extractor"
        ]
        == "knowledge_librarian"
    )

    print()

    print(
        f"Extracted {len(result.claims)} claims"
    )

    for index, claim in enumerate(
        result.claims,
        start=1,
    ):

        print()

        print(
            f"Claim {index}"
        )

        print(
            f"Level: {claim.knowledge_level}"
        )

        print(
            f"Domain: {claim.knowledge_domain}"
        )

        print()

        print(claim.text)

    print()

    print(
        "ExtractionService tests passed."
    )


if __name__ == "__main__":
    main()