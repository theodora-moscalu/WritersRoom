from dataclasses import dataclass
from dataclasses import field

from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.extraction.extracted_provenance import (
    ExtractedProvenance,
)


@dataclass
class ExtractedClaim:
    """A claim proposed by the extraction pipeline."""

    text: str

    knowledge_level: KnowledgeLevel

    knowledge_domain: KnowledgeDomain

    explanation: str = ""

    tags: list[str] = field(
        default_factory=list
    )

    provenance: list[
        ExtractedProvenance
    ] = field(
        default_factory=list
    )