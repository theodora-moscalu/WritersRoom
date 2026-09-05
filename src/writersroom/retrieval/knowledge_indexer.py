from writersroom.database.embedding_repository import (
    text_hash,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.retrieval.base_embedding_provider import (
    BaseEmbeddingProvider,
)
from writersroom.retrieval.base_vector_store import (
    BaseVectorStore,
)


class KnowledgeIndexer:
    """Builds the semantic search index from stored claims."""

    def __init__(
        self,
        repository,
        embedding_provider: BaseEmbeddingProvider,
        vector_store: BaseVectorStore,
        embedding_repository,
    ):
        self.repository = repository

        self.embedding_provider = (
            embedding_provider
        )

        self.vector_store = (
            vector_store
        )

        self.embedding_repository = (
            embedding_repository
        )

    def index(self):
        """Index every stored claim."""

        for claim in (
            self.repository.list_claims()
        ):

            self.index_claim(claim)

    def index_claim(
        self,
        claim: Claim,
    ):
        """Index a single claim, reusing a persisted embedding when current."""

        if self.vector_store.contains(
            claim.identity
        ):

            self.vector_store.remove(
                claim.identity
            )

        embedding = self._embedding_for(claim)

        self.vector_store.add(
            claim,
            embedding,
        )

    def _embedding_for(self, claim: Claim):
        """Return a current embedding for a claim, computing it if needed."""

        stored_hash = (
            self.embedding_repository.get_text_hash(
                claim.identity
            )
        )

        if stored_hash == text_hash(claim.text):

            return self.embedding_repository.get(
                claim.identity
            )

        embedding = (
            self.embedding_provider.embed(
                claim.text
            )
        )

        self.embedding_repository.upsert(
            claim.identity,
            claim.text,
            embedding,
        )

        return embedding
