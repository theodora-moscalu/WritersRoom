from abc import ABC
from abc import abstractmethod

from writersroom.retrieval.knowledge_query import (
    KnowledgeQuery,
)
from writersroom.retrieval.retrieval_result import (
    RetrievalResult,
)


class BaseRetriever(ABC):
    """Base class for knowledge retrieval."""

    @abstractmethod
    def retrieve(
        self,
        query: KnowledgeQuery,
    ) -> list[
        RetrievalResult
    ]:
        """Retrieve relevant claims."""

        raise NotImplementedError