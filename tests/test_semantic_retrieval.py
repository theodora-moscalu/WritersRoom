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
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
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
        "Testing semantic retrieval..."
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

    results = retriever.retrieve(
        KnowledgeQuery(
            text="How do I create tension?"
        )
    )

    assert (
        len(results)
        == 1
    )

    result = results[0]

    assert isinstance(
        result,
        RetrievalResult,
    )

    assert (
        result.text
        == "Conflict creates drama."
    )

    assert (
        result.knowledge_level
        == KnowledgeLevel.PRINCIPLE
    )

    assert (
        result.knowledge_domain
        == KnowledgeDomain.CONFLICT
    )

    assert (
        0.0
        <= result.similarity
        <= 1.0
    )

    print()

    print(
        "Retrieved:"
    )

    print(result)

    print()

    print(
        "Semantic retrieval passed."
    )


if __name__ == "__main__":
    main()