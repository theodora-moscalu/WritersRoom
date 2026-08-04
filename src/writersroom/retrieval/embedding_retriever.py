from writersroom.retrieval.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from writersroom.retrieval.base_retriever import (
    BaseRetriever,
)
from writersroom.retrieval.base_vector_store import (
    BaseVectorStore,
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


class EmbeddingRetriever(
    BaseRetriever
):
    """Retrieves claims using semantic embeddings."""

    def __init__(
        self,
        vector_store: BaseVectorStore,
        embedding_provider: (
            BaseEmbeddingProvider
            | None
        ) = None,
    ):
        self.vector_store = (
            vector_store
        )

        self.embedding_provider = (
            embedding_provider
            or OllamaEmbeddingProvider()
        )

    def retrieve(
        self,
        query: KnowledgeQuery,
    ) -> list[
        RetrievalResult
    ]:
        """Retrieve relevant claims."""

        embedding = (
            self.embedding_provider.embed(
                query.text
            )
        )

        return self.vector_store.search(
            embedding,
            query.max_results,
        )