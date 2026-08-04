from writersroom.domains.knowledge.embedding import (
    Embedding,
)


class EmbeddingCache:
    """Caches embeddings by text."""

    def __init__(
        self,
    ):
        self._cache: dict[
            str,
            Embedding,
        ] = {}

    def contains(
        self,
        text: str,
    ) -> bool:
        """Return whether an embedding exists."""

        return (
            text
            in self._cache
        )

    def get(
        self,
        text: str,
    ) -> Embedding:
        """Return a cached embedding."""

        return self._cache[
            text
        ]

    def store(
        self,
        text: str,
        embedding: Embedding,
    ):
        """Store an embedding."""

        self._cache[
            text
        ] = embedding

    def clear(
        self,
    ):
        """Clear the cache."""

        self._cache.clear()

    def count(
        self,
    ) -> int:
        """Return the number of cached embeddings."""

        return len(
            self._cache
        )