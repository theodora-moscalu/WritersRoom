from writersroom.agents.knowledge_librarian import (
    KnowledgeLibrarian,
)
from writersroom.extraction.extraction_result import (
    ExtractionResult,
)
from writersroom.extraction.knowledge_transformer import (
    KnowledgeTransformer,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)


class ExtractionService:
    """Coordinates knowledge extraction."""

    def __init__(self):

        self.librarian = (
            KnowledgeLibrarian()
        )

        self.transformer = (
            KnowledgeTransformer()
        )

    def extract(
        self,
        unit: SourceUnit,
    ) -> ExtractionResult:
        """Extract knowledge from a source unit."""

        records = (
            self.librarian.analyse(
                unit
            )
        )

        claims = [
            self.transformer.transform(
                record,
                unit,
            )
            for record in records
        ]

        return ExtractionResult(
            claims=claims,
            metadata={
                "extractor": (
                    "knowledge_librarian"
                ),
            },
        )