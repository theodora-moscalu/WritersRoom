from abc import ABC
from abc import abstractmethod

from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
)


class BaseVectorStore(ABC):
    """Stores embeddings for semantic retrieval."""

    @abstractmethod
    def add(
        self,
        claim: Claim,
        embedding: Embedding,
    ):
        """Store an embedding."""

        raise NotImplementedError

    @abstractmethod
    def contains(
        self,
        claim_id: str,
    ) -> bool:
        """Return whether a claim is indexed."""

        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        claim_id: str,
    ):
        """Remove a claim from the index."""

        raise NotImplementedError

    @abstractmethod
    def clear(
        self,
    ):
        """Remove every indexed claim."""

        raise NotImplementedError

    @abstractmethod
    def count(
        self,
    ) -> int:
        """Return the number of indexed claims."""

        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        embedding: Embedding,
        limit: int,
    ) -> list[
        RetrievalResult
    ]:
        """Return the nearest claims."""

        raise NotImplementedError