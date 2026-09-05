from support import knowledge_repository

from writersroom.database.embedding_repository import (
    EmbeddingRepository,
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
from writersroom.retrieval.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from writersroom.retrieval.in_memory_vector_store import (
    InMemoryVectorStore,
)
from writersroom.retrieval.knowledge_indexer import (
    KnowledgeIndexer,
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


class FakeEmbeddingProvider(
    BaseEmbeddingProvider
):
    """Counts embedding requests."""

    def __init__(self):
        self.calls = 0

    def embed(self, text: str) -> Embedding:
        self.calls += 1

        return Embedding(
            model="fake",
            vector=[1.0, 2.0, 3.0],
        )


def main():

    print(
        "Testing persistent embeddings..."
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
    ).add_document(
        "Book",
        "Story",
    )

    PassageService(
        repository
    ).add_passage(
        "Book",
        "Story",
        "Conflict creates drama.",
    )

    claim = (
        ClaimService(
            repository
        ).add_claim(
            knowledge_source_name="Book",
            document_name="Story",
            passage_sequence=1,
            text="Conflict creates drama.",
            knowledge_level=KnowledgeLevel.PRINCIPLE,
            knowledge_domain=KnowledgeDomain.CONFLICT,
        ).data
    )

    embeddings = EmbeddingRepository(
        repository.database
    )

    provider = FakeEmbeddingProvider()

    store = InMemoryVectorStore()

    indexer = KnowledgeIndexer(
        repository,
        provider,
        store,
        embeddings,
    )

    #
    # Re-indexing the same claim only embeds once
    #

    indexer.index_claim(claim)
    indexer.index_claim(claim)
    indexer.index_claim(claim)

    assert provider.calls == 1
    assert store.count() == 1

    #
    # A fresh indexer over the same database (a "restart") reuses the
    # persisted embedding and never calls the provider.
    #

    restart_provider = FakeEmbeddingProvider()

    restart_indexer = KnowledgeIndexer(
        repository,
        restart_provider,
        InMemoryVectorStore(),
        EmbeddingRepository(
            repository.database
        ),
    )

    restart_indexer.index()

    assert restart_provider.calls == 0
    assert restart_indexer.vector_store.count() == 1

    print()

    print(
        "Persistent embedding test passed."
    )


if __name__ == "__main__":
    main()
