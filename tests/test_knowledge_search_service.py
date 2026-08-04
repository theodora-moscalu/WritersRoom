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
from writersroom.retrieval.embedding_retriever import (
    EmbeddingRetriever,
)
from writersroom.retrieval.in_memory_vector_store import (
    InMemoryVectorStore,
)
from writersroom.retrieval.knowledge_indexer import (
    KnowledgeIndexer,
)
from writersroom.retrieval.knowledge_query import (
    KnowledgeQuery,
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
from writersroom.services.knowledge_search_service import (
    KnowledgeSearchService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)


def main():

    print(
        "Testing KnowledgeSearchService..."
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

    ClaimService(
        workspace
    ).add_claim(
        knowledge_source_name="Book",
        document_name="Story",
        passage_sequence=1,
        text="Conflict creates drama.",
        knowledge_level=KnowledgeLevel.PRINCIPLE,
        knowledge_domain=KnowledgeDomain.CONFLICT,
    )

    repository = (
        ClaimRepository(
            workspace
        )
    )

    provider = (
        OllamaEmbeddingProvider()
    )

    store = (
        InMemoryVectorStore()
    )

    KnowledgeIndexer(
        repository,
        provider,
        store,
    ).index()

    retriever = (
        EmbeddingRetriever(
            store,
            provider,
        )
    )

    service = (
        KnowledgeSearchService(
            retriever
        )
    )

    results = service.search(
        KnowledgeQuery(
            text="conflict"
        )
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
        "Retrieved:"
    )

    print(
        results[0]
    )

    print()

    print(
        "KnowledgeSearchService tests passed."
    )


if __name__ == "__main__":
    main()