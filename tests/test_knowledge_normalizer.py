from writersroom.extraction.normalizers.knowledge_normalizer import (
    KnowledgeNormalizer,
)


def main():

    print(
        "Testing KnowledgeNormalizer..."
    )

    response = """
--------------------------------------------------

LEVEL
OBSERV

DOMAIN
CHAR

IMPORT
MED

TEXT
The protagonist is introduced alone.

EXPLANATION
The opening establishes isolation.

--------------------------------------------------
"""

    normalizer = (
        KnowledgeNormalizer()
    )

    normalized = (
        normalizer.normalize(
            response
        )
    )

    print()

    print(
        "Normalized output:"
    )

    print()

    print(
        normalized
    )

    print()

    assert (
        "LEVEL:"
        in normalized
    )

    assert (
        "DOMAIN:"
        in normalized
    )

    assert (
        "IMPORTANCE:"
        in normalized
    )

    assert (
        "TEXT:"
        in normalized
    )

    assert (
        "EXPLANATION:"
        in normalized
    )

    assert (
        "OBSERVATION"
        in normalized
    )

    assert (
        "CHARACTER"
        in normalized
    )

    assert (
        "MEDIUM"
        in normalized
    )

    print(
        "KnowledgeNormalizer tests passed."
    )


if __name__ == "__main__":
    main()