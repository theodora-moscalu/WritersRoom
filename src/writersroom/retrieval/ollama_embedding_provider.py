from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.llm.ollama_embedding_client import (
    OllamaEmbeddingClient,
)
from writersroom.retrieval.base_embedding_provider import (
    BaseEmbeddingProvider,
)


class OllamaEmbeddingProvider(
    BaseEmbeddingProvider
):
    """Embedding provider backed by Ollama."""

    def __init__(
        self,
    ):
        self.client = (
            OllamaEmbeddingClient()
        )

    def embed(
        self,
        text: str,
    ) -> Embedding:
        """Generate an embedding."""

        return self.client.embed(
            text
        )