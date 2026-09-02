from writersroom.agents.knowledge_librarian import (
    KnowledgeLibrarian,
)
from writersroom.extraction.extraction_batch import (
    ExtractionBatch,
)
from writersroom.extraction.extraction_result import (
    ExtractionResult,
)
from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
)
from writersroom.extraction.knowledge_transformer import (
    KnowledgeTransformer,
)


class ExtractionService:
    """Coordinates knowledge extraction."""

    def __init__(
        self,
        librarian: KnowledgeLibrarian | None = None,
        transformer: KnowledgeTransformer | None = None,
    ):

        self.librarian = (
            librarian
            or KnowledgeLibrarian()
        )

        self.transformer = (
            transformer
            or KnowledgeTransformer()
        )

    def extract(
        self,
        unit: ExtractionUnit,
    ) -> ExtractionResult:
        """Extract knowledge from one unit."""

        return self.extract_batch(
            ExtractionBatch(
                [unit]
            )
        )

    def extract_batch(
        self,
        batch: ExtractionBatch,
    ) -> ExtractionResult:
        """Extract knowledge from a batch."""

        claims = []

        for unit in batch:

            records = (
                self.librarian.analyse(
                    unit
                )
            )

            claims.extend(
                self.transformer.transform(
                    record,
                    unit,
                )
                for record in records
            )

        return ExtractionResult(
            claims=claims,
            metadata={
                "extractor": (
                    "knowledge_librarian"
                ),
            },
        )