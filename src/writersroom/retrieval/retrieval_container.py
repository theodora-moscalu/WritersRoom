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
from writersroom.retrieval.ollama_embedding_provider import (
    OllamaEmbeddingProvider,
)
from writersroom.services.knowledge_search_service import (
    KnowledgeSearchService,
)


class RetrievalContainer:
    """Builds the retrieval subsystem."""

    def __init__(
        self,
        workspace: Workspace,
    ):
        self.repository = (
            ClaimRepository(
                workspace
            )
        )

        self.provider = (
            OllamaEmbeddingProvider()
        )

        self.vector_store = (
            InMemoryVectorStore()
        )

        self.indexer = (
            KnowledgeIndexer(
                self.repository,
                self.provider,
                self.vector_store,
            )
        )

        self.retriever = (
            EmbeddingRetriever(
                self.vector_store,
                self.provider,
            )
        )

        self.search_service = (
            KnowledgeSearchService(
                self.retriever,
            )
        )