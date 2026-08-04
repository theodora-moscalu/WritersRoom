from writersroom.retrieval.base_retriever import (
    BaseRetriever,
)
from writersroom.retrieval.knowledge_query import (
    KnowledgeQuery,
)
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
)


class KnowledgeSearchService:
    """Searches the knowledge library."""

    def __init__(
        self,
        retriever: BaseRetriever,
    ):
        self.retriever = retriever

    def search(
        self,
        query: KnowledgeQuery,
    ) -> list[
        RetrievalResult
    ]:
        """Search for relevant knowledge."""

        return self.retriever.retrieve(
            query
        )