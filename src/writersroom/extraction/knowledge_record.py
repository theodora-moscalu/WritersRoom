from dataclasses import dataclass

from writersroom.domains.enums.importance import (
    Importance,
)
from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)


@dataclass
class KnowledgeRecord:
    """A single piece of knowledge proposed by an AI agent."""

    knowledge_level: KnowledgeLevel

    knowledge_domain: KnowledgeDomain

    importance: Importance

    text: str

    explanation: str