from dataclasses import dataclass
from dataclasses import field

from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)


@dataclass
class KnowledgeQuery:
    """A request for storytelling knowledge."""

    text: str

    max_results: int = 10

    knowledge_domains: list[
        KnowledgeDomain
    ] = field(
        default_factory=list
    )

    knowledge_levels: list[
        KnowledgeLevel
    ] = field(
        default_factory=list
    )