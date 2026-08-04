from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.review.review_decision import (
    ReviewDecision,
)
from writersroom.review.review_result import (
    ReviewResult,
)
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.extraction_service import (
    ExtractionService,
)
from writersroom.services.review_service import (
    ReviewService,
)


class KnowledgePipelineService:
    """Coordinates the knowledge pipeline."""

    def __init__(
        self,
        workspace,
    ):
        self.claim_service = (
            ClaimService(
                workspace
            )
        )

        self.extraction_service = (
            ExtractionService()
        )

        self.review_service = (
            ReviewService()
        )

    def process(
        self,
        knowledge_source_name: str,
        document_name: str,
        processed_document: ProcessedDocument,
    ) -> ReviewResult:
        """Process a document through the knowledge pipeline."""

        items = []

        for unit in (
            processed_document.source_units
        ):

            extraction = (
                self.extraction_service.extract(
                    unit
                )
            )

            review = (
                self.review_service.review(
                    extraction
                )
            )

            for item in review.accepted_items:

                self.claim_service.add_extracted_claim(
                    knowledge_source_name=knowledge_source_name,
                    document_name=document_name,
                    extracted=item.claim,
                )

            items.extend(
                review.items
            )

        return ReviewResult(
            items=items,
        )