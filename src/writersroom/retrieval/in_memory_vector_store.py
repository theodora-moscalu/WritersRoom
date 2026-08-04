from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.retrieval.base_similarity_calculator import (
    BaseSimilarityCalculator,
)
from writersroom.retrieval.base_vector_store import (
    BaseVectorStore,
)
from writersroom.retrieval.cosine_similarity_calculator import (
    CosineSimilarityCalculator,
)
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
)
from writersroom.retrieval.vector_record import (
    VectorRecord,
)


class InMemoryVectorStore(
    BaseVectorStore
):
    """Simple in-memory vector store."""

    def __init__(
        self,
        calculator: BaseSimilarityCalculator | None = None,
    ):
        self._records: dict[
            str,
            VectorRecord,
        ] = {}

        self.calculator = (
            calculator
            or CosineSimilarityCalculator()
        )

    def add(
        self,
        claim: Claim,
        embedding: Embedding,
    ):
        """Store an embedding."""

        self._records[
            claim.identity
        ] = VectorRecord(
            claim=claim,
            embedding=embedding,
        )

    def contains(
        self,
        claim_id: str,
    ) -> bool:
        """Return whether a claim is indexed."""

        return (
            claim_id
            in self._records
        )

    def remove(
        self,
        claim_id: str,
    ):
        """Remove a claim."""

        self._records.pop(
            claim_id,
            None,
        )

    def clear(
        self,
    ):
        """Remove every indexed claim."""

        self._records.clear()

    def count(
        self,
    ) -> int:
        """Return the number of indexed claims."""

        return len(
            self._records
        )

    def search(
        self,
        embedding: Embedding,
        limit: int,
    ) -> list[
        RetrievalResult
    ]:
        """Return the nearest claims."""

        return self.calculator.search(
            embedding,
            list(
                self._records.values()
            ),
            limit,
        )