from writersroom.extraction.extraction_batch import (
    ExtractionBatch,
)
from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
)


class ExtractionBatcher:
    """Groups extraction units into batches."""

    def create_batches(
        self,
        units: list[ExtractionUnit],
        batch_size: int,
    ) -> list[ExtractionBatch]:

        batches = []

        for index in range(
            0,
            len(units),
            batch_size,
        ):

            batches.append(
                ExtractionBatch(
                    units[
                        index:index + batch_size
                    ]
                )
            )

        return batches