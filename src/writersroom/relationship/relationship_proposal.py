from writersroom.domains.enums.knowledge_relationship_type import (
    KnowledgeRelationshipType,
)


class RelationshipProposal:
    """A proposed relationship between two knowledge claims."""

    def __init__(
        self,
        source_claim_id: str,
        target_claim_id: str,
        relationship_type: KnowledgeRelationshipType,
        confidence: float,
        reasoning: str,
    ):
        self.source_claim_id = source_claim_id
        self.target_claim_id = target_claim_id
        self.relationship_type = relationship_type
        self.confidence = confidence
        self.reasoning = reasoning