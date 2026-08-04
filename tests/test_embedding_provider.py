from writersroom.retrieval.ollama_embedding_provider import (
    OllamaEmbeddingProvider,
)


def main():

    print(
        "Testing OllamaEmbeddingProvider..."
    )

    provider = (
        OllamaEmbeddingProvider()
    )

    embedding = provider.embed(
        "Conflict creates drama."
    )

    assert (
        embedding.model
        == "nomic-embed-text"
    )

    assert (
        embedding.dimensions
        > 0
    )

    assert (
        len(
            embedding.vector
        )
        == embedding.dimensions
    )

    print()

    print(
        f"Model: {embedding.model}"
    )

    print(
        f"Dimensions: {embedding.dimensions}"
    )

    print()

    print(
        "EmbeddingProvider tests passed."
    )


if __name__ == "__main__":
    main()