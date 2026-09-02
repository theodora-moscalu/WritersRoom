from writersroom.agents.base_agent import (
    Agent,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.relationship.relationship_record import (
    RelationshipRecord,
)


class RelationshipAnalyser(
    Agent
):
    """AI agent responsible for analysing the relationship between two claims."""

    def __init__(
        self,
    ):
        super().__init__(
            name=(
                "Relationship Analyser"
            ),
            prompt_file=(
                "relationship_analyser.txt"
            ),
        )

    def analyse(
        self,
        claim_a: Claim,
        claim_b: Claim,
    ) -> list[
        RelationshipRecord
    ]:
        """Analyse the relationship between two claims."""

        #
        # We'll implement the
        # LLM interaction next.
        #

        return []