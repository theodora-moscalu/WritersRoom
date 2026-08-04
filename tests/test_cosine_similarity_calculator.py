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
from writersroom.retrieval.cosine_similarity_calculator import (
    CosineSimilarityCalculator,
)
from writersroom.retrieval.vector_record import (
    VectorRecord,
)


def main():

    print(
        "Testing CosineSimilarityCalculator..."
    )

    calculator = (
        CosineSimilarityCalculator()
    )

    record = VectorRecord(
        claim=Claim(
            identity="CLM-1",
            passage_id="PAS-1",
            text="Conflict",
            knowledge_level=KnowledgeLevel.PRINCIPLE,
            knowledge_domain=KnowledgeDomain.CONFLICT,
        ),
        embedding=Embedding(
            model="test",
            vector=[
                1.0,
                0.0,
            ],
        ),
    )

    query = Embedding(
        model="test",
        vector=[
            1.0,
            0.0,
        ],
    )

    results = calculator.search(
        query,
        [record],
        1,
    )

    assert (
        len(results)
        == 1
    )

    assert (
        results[0].claim.text
        == "Conflict"
    )

    print()

    print(
        "CosineSimilarityCalculator tests passed."
    )


if __name__ == "__main__":
    main()