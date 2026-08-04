from abc import ABC
from abc import abstractmethod

from writersroom.domains.knowledge.embedding import (
    Embedding,
)


class BaseEmbeddingProvider(ABC):
    """Base class for embedding providers."""

    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> Embedding:
        """Generate an embedding."""

        raise NotImplementedError