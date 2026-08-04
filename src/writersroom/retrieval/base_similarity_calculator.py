from abc import ABC
from abc import abstractmethod

from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
)
from writersroom.retrieval.vector_record import (
    VectorRecord,
)


class BaseSimilarityCalculator(ABC):
    """Ranks vectors by similarity."""

    @abstractmethod
    def search(
        self,
        query: Embedding,
        records: list[VectorRecord],
        limit: int,
    ) -> list[RetrievalResult]:
        """Return the nearest records."""

        raise NotImplementedError