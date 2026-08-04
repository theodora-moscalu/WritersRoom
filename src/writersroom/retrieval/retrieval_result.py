from dataclasses import dataclass

from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.provenance import (
    Provenance,
)


@dataclass(frozen=True)
class RetrievalResult:
    """Represents a retrieved claim and its similarity score."""

    claim: Claim

    similarity: float

    @property
    def identity(
        self,
    ) -> str:
        """Return the claim identity."""

        return self.claim.identity

    @property
    def text(
        self,
    ) -> str:
        """Return the claim text."""

        return self.claim.text

    @property
    def explanation(
        self,
    ) -> str:
        """Return the claim explanation."""

        return self.claim.explanation

    @property
    def knowledge_level(
        self,
    ) -> KnowledgeLevel:
        """Return the claim's knowledge level."""

        return (
            self.claim.knowledge_level
        )

    @property
    def knowledge_domain(
        self,
    ) -> KnowledgeDomain:
        """Return the claim's knowledge domain."""

        return (
            self.claim.knowledge_domain
        )

    @property
    def provenance(
        self,
    ) -> list[Provenance]:
        """Return the claim provenance."""

        return (
            self.claim.provenance
        )

    def __str__(
        self,
    ) -> str:

        return (
            f"[{self.similarity:.3f}] "
            f"{self.knowledge_domain.name}/"
            f"{self.knowledge_level.name} "
            f"{self.text}"
        )