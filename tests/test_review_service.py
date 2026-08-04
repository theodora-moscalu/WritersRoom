from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.extraction.extraction_result import (
    ExtractionResult,
)
from writersroom.services.review_service import (
    ReviewService,
)


def main():
    print("Testing ReviewService...")

    service = ReviewService()

    claim = ExtractedClaim(
        text=(
            "A protagonist should pursue "
            "a concrete objective."
        ),
        confidence=1.0,
    )

    extraction = ExtractionResult(
        claims=[claim]
    )

    result = service.review(
        extraction
    )

    assert (
        len(result.accepted_claims)
        == 1
    )

    assert (
        len(result.rejected_claims)
        == 0
    )

    accepted = (
        result.accepted_claims[0]
    )

    assert (
        accepted.text
        == (
            "A protagonist should pursue "
            "a concrete objective."
        )
    )

    assert (
        accepted.confidence
        == 1.0
    )

    print(
        "ReviewService tests passed."
    )


if __name__ == "__main__":
    main()