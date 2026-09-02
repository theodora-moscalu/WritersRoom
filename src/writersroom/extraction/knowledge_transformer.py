from writersroom.extraction.extracted_claim import (
    ExtractedClaim,
)
from writersroom.extraction.extracted_provenance import (
    ExtractedProvenance,
)
from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
)
from writersroom.extraction.knowledge_record import (
    KnowledgeRecord,
)


class KnowledgeTransformer:
    """Transforms AI knowledge into extracted claims."""

    def transform(
        self,
        record: KnowledgeRecord,
        unit: ExtractionUnit,
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
                    passage_sequence=sequence,
                    confidence=1.0,
                )
                for sequence in (
                    unit.passage_sequences
                )
            ],
        )