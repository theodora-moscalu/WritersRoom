from writersroom.domains.enums.knowledge_type import (
    KnowledgeType,
)


def main():
    print(
        "Testing KnowledgeType..."
    )

    assert (
        KnowledgeType.STRUCTURE
        == "structure"
    )

    assert (
        KnowledgeType.CONFLICT
        == "conflict"
    )

    assert (
        KnowledgeType.PACING
        == "pacing"
    )

    print(
        "KnowledgeType tests passed."
    )


if __name__ == "__main__":
    main()