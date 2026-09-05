from support import knowledge_repository

from writersroom.database.embedding_repository import (
    EmbeddingRepository,
    text_hash,
)
from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)


def main():

    print(
        "Testing EmbeddingRepository..."
    )

    repository = knowledge_repository()

    KnowledgeSourceService(
        repository
    ).add_source(
        "Book",
        KnowledgeSourceType.BOOK,
    )

    DocumentService(
        repository
    ).add_document("Book", "Story")

    PassageService(
        repository
    ).add_passage(
        "Book",
        "Story",
        "Conflict creates drama.",
    )

    claim = (
        ClaimService(repository)
        .add_claim(
            knowledge_source_name="Book",
            document_name="Story",
            passage_sequence=1,
            text="Conflict creates drama.",
            knowledge_level=KnowledgeLevel.PRINCIPLE,
            knowledge_domain=KnowledgeDomain.CONFLICT,
        )
        .data
    )

    embeddings = EmbeddingRepository(
        repository.database
    )

    assert embeddings.get(claim.identity) is None

    embeddings.upsert(
        claim.identity,
        claim.text,
        Embedding(
            model="test",
            vector=[0.25, 0.5, 0.75],
        ),
    )

    stored = embeddings.get(claim.identity)

    assert stored.model == "test"
    assert stored.dimensions == 3
    assert len(stored.vector) == 3
    assert abs(stored.vector[1] - 0.5) < 1e-6

    assert (
        embeddings.get_text_hash(claim.identity)
        == text_hash(claim.text)
    )

    #
    # A cascade delete of the claim removes the embedding.
    #

    repository.delete_claim(claim.identity)

    assert embeddings.get(claim.identity) is None

    print()

    print(
        "EmbeddingRepository tests passed."
    )


if __name__ == "__main__":
    main()
