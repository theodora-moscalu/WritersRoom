import ollama

from writersroom.domains.knowledge.embedding import (
    Embedding,
)


class OllamaEmbeddingClient:
    """Client for Ollama embeddings."""

    DEFAULT_MODEL = (
        "nomic-embed-text"
    )

    def embed(
        self,
        text: str,
        model: str = DEFAULT_MODEL,
    ) -> Embedding:
        """Generate an embedding."""

        response = ollama.embed(
            model=model,
            input=text,
        )

        vector = response[
            "embeddings"
        ][0]

        return Embedding(
            model=model,
            vector=vector,
        )