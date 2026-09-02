from writersroom.extraction.extraction_granularity import (
    ExtractionGranularity,
)
from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
)
from writersroom.extraction.extraction_unit_selector import (
    ExtractionUnitSelector,
)
from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.review.review_result import (
    ReviewResult,
)

from writersroom.services.extraction_service import (
    ExtractionService,
)
from writersroom.services.parallel_extraction_executor import (
    ParallelExtractionExecutor,
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
        self.extraction_service = (
            ExtractionService()
        )

        self.review_service = (
            ReviewService()
        )

        self.selector = (
            ExtractionUnitSelector()
        )

        self.executor = (
            ParallelExtractionExecutor(
                max_workers=4,
            )
        )

    def _process_unit(
        self,
        unit: ExtractionUnit,
    ):
        """Process a single extraction unit."""

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

        return (
            unit,
            review,
        )

    def process(
        self,
        knowledge_source_name: str,
        document_name: str,
        processed_document: ProcessedDocument,
        granularity: (
            ExtractionGranularity
        ) = (
            ExtractionGranularity.SOURCE_UNIT
        ),
    ) -> ReviewResult:
        """Process a document through the knowledge pipeline."""

        units = self.selector.select(
            processed_document,
            granularity,
        )

        total = len(
            units
        )

        print()

        results = (
            self.executor.execute(
                units,
                self._process_unit,
            )
        )

        items = []

        for index, (
            unit,
            review,
        ) in enumerate(
            results,
            start=1,
        ):

            print(
                f"[{index:03}/{total:03}] ",
                end="",
            )

            if unit.heading:

                print(
                    unit.heading
                )

            else:

                print(
                    f"Unit {index}"
                )

            print(
                f"          Candidates: "
                f"{len(review.items)}"
            )

            items.extend(
                review.items
            )

            print()

        return ReviewResult(
            items=items,
        )