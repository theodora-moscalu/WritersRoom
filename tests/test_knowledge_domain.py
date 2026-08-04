from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)


def main():
    print(
        "Testing KnowledgeDomain..."
    )

    assert (
        KnowledgeDomain.UNKNOWN
        == "unknown"
    )

    assert (
        KnowledgeDomain.STRUCTURE
        == "structure"
    )

    assert (
        KnowledgeDomain.CHARACTER
        == "character"
    )

    assert (
        KnowledgeDomain.WRITING
        == "writing"
    )

    print(
        "KnowledgeDomain tests passed."
    )


if __name__ == "__main__":
    main()