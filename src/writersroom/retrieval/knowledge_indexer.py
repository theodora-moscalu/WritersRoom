from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.document import (
    Document,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)
from writersroom.retrieval.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from writersroom.retrieval.base_vector_store import (
    BaseVectorStore,
)
from writersroom.retrieval.claim_repository import (
    ClaimRepository,
)
from writersroom.retrieval.embedding_cache import (
    EmbeddingCache,
)


class KnowledgeIndexer:
    """Builds the semantic search index."""

    def __init__(
        self,
        repository: ClaimRepository,
        embedding_provider: BaseEmbeddingProvider,
        vector_store: BaseVectorStore,
        embedding_cache: (
            EmbeddingCache | None
        ) = None,
    ):
        self.repository = repository

        self.embedding_provider = (
            embedding_provider
        )

        self.vector_store = (
            vector_store
        )

        self.embedding_cache = (
            embedding_cache
            or EmbeddingCache()
        )

    def index(
        self,
    ):
        """Index every stored claim."""

        for source in (
            self.repository.list_sources()
        ):

            self.index_source(
                source
            )

    def index_source(
        self,
        source: KnowledgeSource,
    ):
        """Index every claim in a knowledge source."""

        for document in (
            source.list_documents()
        ):

            self.index_document(
                document
            )

    def index_document(
        self,
        document: Document,
    ):
        """Index every claim in a document."""

        for claim in (
            self.repository.list_document_claims(
                document
            )
        ):

            self.index_claim(
                claim
            )

    def index_claim(
        self,
        claim: Claim,
    ):
        """Index a single claim."""

        if self.vector_store.contains(
            claim.identity
        ):

            self.vector_store.remove(
                claim.identity
            )

        if self.embedding_cache.contains(
            claim.text
        ):

            embedding = (
                self.embedding_cache.get(
                    claim.text
                )
            )

        else:

            embedding = (
                self.embedding_provider.embed(
                    claim.text
                )
            )

            self.embedding_cache.store(
                claim.text,
                embedding,
            )

        self.vector_store.add(
            claim,
            embedding,
        )