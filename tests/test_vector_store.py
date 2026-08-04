from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.retrieval.in_memory_vector_store import (
    InMemoryVectorStore,
)
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
)


def main():

    print(
        "Testing InMemoryVectorStore..."
    )

    store = (
        InMemoryVectorStore()
    )

    claim = Claim(
        identity="CLM-1",
        passage_id="PAS-1",
        text="Conflict creates drama.",
        knowledge_level=(
            KnowledgeLevel.PRINCIPLE
        ),
        knowledge_domain=(
            KnowledgeDomain.CONFLICT
        ),
    )

    embedding = Embedding(
        model="test",
        vector=[
            0.1,
            0.2,
            0.3,
        ],
    )

    #
    # Add
    #

    store.add(
        claim,
        embedding,
    )

    assert (
        store.count()
        == 1
    )

    assert (
        store.contains(
            claim.identity
        )
    )

    #
    # Search
    #

    results = store.search(
        embedding,
        limit=5,
    )

    assert (
        len(results)
        == 1
    )

    result = results[0]

    assert isinstance(
        result,
        RetrievalResult,
    )

    assert (
        result.text
        == "Conflict creates drama."
    )

    assert (
        result.knowledge_level
        == KnowledgeLevel.PRINCIPLE
    )

    assert (
        result.knowledge_domain
        == KnowledgeDomain.CONFLICT
    )

    assert (
        result.similarity
        == 1.0
    )

    #
    # Remove
    #

    store.remove(
        claim.identity
    )

    assert (
        store.count()
        == 0
    )

    assert (
        not store.contains(
            claim.identity
        )
    )

    #
    # Clear
    #

    store.add(
        claim,
        embedding,
    )

    assert (
        store.count()
        == 1
    )

    store.clear()

    assert (
        store.count()
        == 0
    )

    print()

    print(
        "VectorStore tests passed."
    )


if __name__ == "__main__":
    main()