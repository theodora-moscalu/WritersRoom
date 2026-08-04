from dataclasses import dataclass

from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.embedding import (
    Embedding,
)


@dataclass
class VectorRecord:
    """A stored semantic vector."""

    claim: Claim

    embedding: Embedding