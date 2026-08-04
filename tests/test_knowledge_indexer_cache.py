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
from writersroom.domains.workspace import (
    Workspace,
)
from writersroom.retrieval.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from writersroom.retrieval.claim_repository import (
    ClaimRepository,
)
from writersroom.retrieval.embedding_cache import (
    EmbeddingCache,
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

    def __init__(
        self,
    ):
        self.calls = 0

    def embed(
        self,
        text: str,
    ) -> Embedding:

        self.calls += 1

        return Embedding(
            model="fake",
            vector=[
                1.0,
                2.0,
                3.0,
            ],
        )


def main():

    print(
        "Testing embedding cache..."
    )

    workspace = Workspace()

    KnowledgeSourceService(
        workspace
    ).add_source(
        "Book",
        KnowledgeSourceType.BOOK,
    )

    DocumentService(
        workspace
    ).add_document(
        "Book",
        "Story",
    )

    PassageService(
        workspace
    ).add_passage(
        "Book",
        "Story",
        "Conflict creates drama.",
    )

    claim = (
        ClaimService(
            workspace
        ).add_claim(
            knowledge_source_name="Book",
            document_name="Story",
            passage_sequence=1,
            text="Conflict creates drama.",
            knowledge_level=KnowledgeLevel.PRINCIPLE,
            knowledge_domain=KnowledgeDomain.CONFLICT,
        ).data
    )

    provider = (
        FakeEmbeddingProvider()
    )

    cache = (
        EmbeddingCache()
    )

    store = (
        InMemoryVectorStore()
    )

    repository = (
        ClaimRepository(
            workspace
        )
    )

    indexer = (
        KnowledgeIndexer(
            repository,
            provider,
            store,
            cache,
        )
    )

    indexer.index_claim(
        claim
    )

    indexer.index_claim(
        claim
    )

    indexer.index_claim(
        claim
    )

    assert (
        provider.calls
        == 1
    )

    assert (
        cache.count()
        == 1
    )

    assert (
        store.count()
        == 1
    )

    print()

    print(
        "Embedding cache test passed."
    )


if __name__ == "__main__":
    main()