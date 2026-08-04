from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.extraction.extracted_provenance import (
    ExtractedProvenance,
)
from writersroom.extraction.knowledge_record import (
    KnowledgeRecord,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)


class KnowledgeTransformer:
    """Transforms AI knowledge into extracted claims."""

    def transform(
        self,
        record: KnowledgeRecord,
        unit: SourceUnit,
    ) -> ExtractedClaim:
        """Transform a knowledge record into an extracted claim."""

        return ExtractedClaim(
            text=record.text,
            explanation=record.explanation,
            knowledge_level=(
                record.knowledge_level
            ),
            knowledge_domain=(
                record.knowledge_domain
            ),
            provenance=[
                ExtractedProvenance(
                    passage_sequence=(
                        unit.sequence
                    ),
                    confidence=1.0,
                )
            ],
        )