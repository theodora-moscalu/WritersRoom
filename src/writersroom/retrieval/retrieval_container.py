from writersroom.database.embedding_repository import (
    EmbeddingRepository,
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
        repository,
    ):
        self.repository = repository

        self.embedding_repository = (
            EmbeddingRepository(
                repository.database
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
                self.embedding_repository,
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

    def build_index(self):
        """Populate the in-memory vector store from persisted embeddings."""

        self.indexer.index()
