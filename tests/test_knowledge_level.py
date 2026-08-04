from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)


def main():
    print(
        "Testing KnowledgeLevel..."
    )

    assert (
        KnowledgeLevel.OBSERVATION
        == "observation"
    )

    assert (
        KnowledgeLevel.PATTERN
        == "pattern"
    )

    assert (
        KnowledgeLevel.PRINCIPLE
        == "principle"
    )

    print(
        "KnowledgeLevel tests passed."
    )


if __name__ == "__main__":
    main()