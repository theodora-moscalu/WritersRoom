from writersroom.domains.enums.knowledge_relationship_type import (
    KnowledgeRelationshipType,
)


def main():

    print(
        "Testing KnowledgeRelationshipType..."
    )

    assert (
        KnowledgeRelationshipType.SIMILAR_TO.value
        == "Similar To"
    )

    assert (
        KnowledgeRelationshipType.SUPPORTS.value
        == "Supports"
    )

    assert (
        KnowledgeRelationshipType.CONTRADICTS.value
        == "Contradicts"
    )

    print()

    print(
        "KnowledgeRelationshipType tests passed."
    )


if __name__ == "__main__":
    main()