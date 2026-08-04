from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.retrieval.knowledge_query import (
    KnowledgeQuery,
)


def main():

    print(
        "Testing KnowledgeQuery..."
    )

    query = KnowledgeQuery(
        text=(
            "introducing protagonists"
        ),
        max_results=5,
        knowledge_domains=[
            KnowledgeDomain.CHARACTER,
        ],
        knowledge_levels=[
            KnowledgeLevel.PRINCIPLE,
        ],
    )

    assert (
        query.text
        == "introducing protagonists"
    )

    assert (
        query.max_results
        == 5
    )

    assert (
        query.knowledge_domains[0]
        == KnowledgeDomain.CHARACTER
    )

    assert (
        query.knowledge_levels[0]
        == KnowledgeLevel.PRINCIPLE
    )

    print(
        "KnowledgeQuery tests passed."
    )


if __name__ == "__main__":
    main()