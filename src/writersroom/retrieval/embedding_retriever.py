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

        has_filters = bool(
            query.knowledge_domains
            or query.knowledge_levels
        )

        limit = (
            max(query.max_results * 5, 50)
            if has_filters
            else query.max_results
        )

        results = self.vector_store.search(
            embedding,
            limit,
        )

        if not has_filters:
            return results

        filtered = [
            result
            for result in results
            if self._matches(result, query)
        ]

        return filtered[: query.max_results]

    def _matches(
        self,
        result: RetrievalResult,
        query: KnowledgeQuery,
    ) -> bool:
        """Check a result against the query's domain and level filters."""

        if (
            query.knowledge_domains
            and result.knowledge_domain
            not in query.knowledge_domains
        ):
            return False

        if (
            query.knowledge_levels
            and result.knowledge_level
            not in query.knowledge_levels
        ):
            return False

        return True
