from support import knowledge_repository

from writersroom.agents.knowledge_context import (
    KnowledgeContextBuilder,
)
from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.embedding import (
    Embedding,
)
from writersroom.retrieval.base_embedding_provider import (
    BaseEmbeddingProvider,
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
from writersroom.database.embedding_repository import (
    EmbeddingRepository,
)
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_search_service import (
    KnowledgeSearchService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)


class TopicEmbeddingProvider(BaseEmbeddingProvider):
    """Embeds on a single keyword so similarity is predictable."""

    def embed(self, text: str) -> Embedding:
        conflict = 1.0 if "conflict" in text.lower() else 0.0

        return Embedding(
            model="fake",
            vector=[conflict, 1.0 - conflict],
        )


def seed_claim(repository, source, text, domain):
    KnowledgeSourceService(repository).add_source(
        source, KnowledgeSourceType.SCREENPLAY
    )
    DocumentService(repository).add_document(source, "Script")
    PassageService(repository).add_passage(source, "Script", text)

    return (
        ClaimService(repository)
        .add_claim(
            knowledge_source_name=source,
            document_name="Script",
            passage_sequence=1,
            text=text,
            knowledge_level=KnowledgeLevel.PRINCIPLE,
            knowledge_domain=domain,
            explanation="Demonstrated by the scene.",
        )
        .data
    )


def main():
    print("Testing KnowledgeContextBuilder...")

    repository = knowledge_repository()

    provider = TopicEmbeddingProvider()
    store = InMemoryVectorStore()

    #
    # Empty library -> empty block
    #

    search_service = KnowledgeSearchService(
        EmbeddingRetriever(store, provider)
    )

    builder = KnowledgeContextBuilder(
        search_service,
        repository,
    )

    assert builder.build("How do I raise the stakes?") == ""

    #
    # Seed two claims, index them
    #

    conflict_claim = seed_claim(
        repository,
        "Whiplash",
        "Escalating conflict between mentor and student drives the drama.",
        KnowledgeDomain.CONFLICT,
    )

    seed_claim(
        repository,
        "Chinatown",
        "A visual motif can foreshadow a thematic reveal.",
        KnowledgeDomain.VISUAL,
    )

    KnowledgeIndexer(
        repository,
        provider,
        store,
        EmbeddingRepository(repository.database),
    ).index()

    #
    # A conflict question surfaces only the conflict claim, with its source
    #

    block = builder.build(
        "How should the conflict between them escalate?"
    )

    assert conflict_claim.identity in block
    assert "Whiplash" in block
    assert "Chinatown" not in block
    assert "Demonstrated by the scene." in block
    assert "CRAFT" in block

    #
    # A thin question does not surface the conflict claim; the scene steers it there
    #

    unsteered = builder.build("does this land?")
    assert conflict_claim.identity not in unsteered

    steered = builder.build(
        "does this land?",
        context_text="A scene of escalating conflict between the two of them.",
    )
    assert conflict_claim.identity in steered

    print()
    print(block)
    print()

    print("KnowledgeContextBuilder tests passed.")


if __name__ == "__main__":
    main()
