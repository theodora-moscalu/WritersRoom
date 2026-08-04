from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.workspace import (
    Workspace,
)
from writersroom.retrieval.claim_repository import (
    ClaimRepository,
)
from writersroom.retrieval.in_memory_vector_store import (
    InMemoryVectorStore,
)
from writersroom.retrieval.knowledge_indexer import (
    KnowledgeIndexer,
)
from writersroom.retrieval.ollama_embedding_provider import (
    OllamaEmbeddingProvider,
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
        "Testing KnowledgeIndexer..."
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

    repository = (
        ClaimRepository(
            workspace
        )
    )

    store = (
        InMemoryVectorStore()
    )

    provider = (
        OllamaEmbeddingProvider()
    )

    indexer = (
        KnowledgeIndexer(
            repository,
            provider,
            store,
        )
    )

    #
    # Full indexing
    #

    indexer.index()

    assert (
        store.count()
        == 1
    )

    #
    # Incremental indexing
    #

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
        store.count()
        == 1
    )

    #
    # Search still works
    #

    results = store.search(
        provider.embed(
            "Conflict creates drama."
        ),
        limit=10,
    )

    assert (
        len(results)
        == 1
    )

    assert (
        results[0].text
        == "Conflict creates drama."
    )

    print()

    print(
        "KnowledgeIndexer tests passed."
    )


if __name__ == "__main__":
    main()