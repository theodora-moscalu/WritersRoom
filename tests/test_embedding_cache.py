from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.retrieval.embedding_cache import (
    EmbeddingCache,
)


def main():

    print(
        "Testing EmbeddingCache..."
    )

    cache = (
        EmbeddingCache()
    )

    text = (
        "Conflict creates drama."
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
    # Initially empty
    #

    assert (
        cache.count()
        == 0
    )

    assert (
        not cache.contains(
            text
        )
    )

    #
    # Store
    #

    cache.store(
        text,
        embedding,
    )

    assert (
        cache.count()
        == 1
    )

    assert (
        cache.contains(
            text
        )
    )

    cached = cache.get(
        text
    )

    assert (
        cached.model
        == "test"
    )

    assert (
        cached.vector
        == [
            0.1,
            0.2,
            0.3,
        ]
    )

    #
    # Clear
    #

    cache.clear()

    assert (
        cache.count()
        == 0
    )

    print()

    print(
        "EmbeddingCache tests passed."
    )


if __name__ == "__main__":
    main()