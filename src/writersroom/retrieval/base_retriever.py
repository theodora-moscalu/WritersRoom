from abc import ABC
from abc import abstractmethod

from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.retrieval.knowledge_query import (
    KnowledgeQuery,
)


class BaseRetriever(ABC):
    """Base class for knowledge retrieval."""

    @abstractmethod
    def retrieve(
        self,
        query: KnowledgeQuery,
    ) -> list[Claim]:
        """Retrieve relevant claims."""

        raise NotImplementedError