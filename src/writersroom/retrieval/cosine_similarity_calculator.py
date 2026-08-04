import math

from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.retrieval.base_similarity_calculator import (
    BaseSimilarityCalculator,
)
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
)
from writersroom.retrieval.vector_record import (
    VectorRecord,
)


class CosineSimilarityCalculator(
    BaseSimilarityCalculator
):
    """Ranks vectors using cosine similarity."""

    def _cosine(
        self,
        left: list[float],
        right: list[float],
    ) -> float:

        numerator = sum(
            a * b
            for a, b in zip(
                left,
                right,
            )
        )

        left_norm = math.sqrt(
            sum(
                a * a
                for a in left
            )
        )

        right_norm = math.sqrt(
            sum(
                b * b
                for b in right
            )
        )

        if (
            left_norm == 0
            or right_norm == 0
        ):
            return 0.0

        return (
            numerator
            / (
                left_norm
                * right_norm
            )
        )

    def search(
        self,
        query: Embedding,
        records: list[
            VectorRecord
        ],
        limit: int,
    ) -> list[
        RetrievalResult
    ]:

        ranked = sorted(
            (
                RetrievalResult(
                    claim=record.claim,
                    similarity=self._cosine(
                        query.vector,
                        record.embedding.vector,
                    ),
                )
                for record in records
            ),
            key=lambda result: (
                result.similarity
            ),
            reverse=True,
        )

        return ranked[
            :limit
        ]