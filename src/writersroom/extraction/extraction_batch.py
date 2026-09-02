from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
)


class ExtractionBatch:
    """A batch of extraction units."""

    def __init__(
        self,
        units: list[ExtractionUnit],
    ):
        self.units = units

    def __iter__(self):
        return iter(
            self.units
        )

    def __len__(self):
        return len(
            self.units
        )