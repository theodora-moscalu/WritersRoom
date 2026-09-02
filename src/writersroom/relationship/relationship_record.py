from dataclasses import dataclass

from writersroom.domains.enums.knowledge_relationship_type import (
    KnowledgeRelationshipType,
)


@dataclass
class RelationshipRecord:
    """Raw relationship extracted by the AI."""

    source_claim_id: str

    target_claim_id: str

    relationship_type: (
        KnowledgeRelationshipType
    )

    confidence: float

    reasoning: str