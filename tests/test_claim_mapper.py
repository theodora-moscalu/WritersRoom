from writersroom.domains.workspace import (
    Workspace,
)
from writersroom.domains.knowledge.passage import (
    Passage,
)
from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.extraction.extracted_provenance import (
    ExtractedProvenance,
)
from writersroom.mappers.claim_mapper import (
    ClaimMapper,
)


def main():
    print("Testing ClaimMapper...")

    workspace = Workspace()

    passage = Passage(
        identity="PSG1",
        document_id="DOC1",
        sequence=1,
        text="Original passage.",
    )

    extracted = ExtractedClaim(
        text=(
            "A protagonist should pursue "
            "a concrete objective."
        ),
        explanation=(
            "Objectives drive story momentum."
        ),
        provenance=[
            ExtractedProvenance(
                passage_sequence=1,
                confidence=0.95,
            ),
            ExtractedProvenance(
                passage_sequence=2,
                confidence=0.87,
            ),
        ],
    )

    claim = ClaimMapper.map(
        workspace=workspace,
        passage=passage,
        extracted=extracted,
    )

    assert (
        claim.text
        == (
            "A protagonist should pursue "
            "a concrete objective."
        )
    )

    assert (
        claim.explanation
        == (
            "Objectives drive story momentum."
        )
    )

    assert (
        claim.passage_id
        == "PSG1"
    )

    assert (
        len(claim.provenance)
        == 2
    )

    assert (
        claim.provenance[0].source_document_id
        == "DOC1"
    )

    assert (
        claim.provenance[0].passage_id
        == "PSG1"
    )

    assert (
        claim.provenance[0].confidence
        == 0.95
    )

    assert (
        claim.provenance[1].confidence
        == 0.87
    )

    assert (
        claim.provenance[0].reviewed
        is True
    )

    print(
        "ClaimMapper tests passed."
    )


if __name__ == "__main__":
    main()