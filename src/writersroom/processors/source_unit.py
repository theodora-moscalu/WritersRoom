from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


class SourceUnit:
    """Represents a unit of source material."""

    def __init__(
        self,
        sequence: int,
        text: str,
        unit_type: SourceUnitType,
        heading: str | None = None,
    ):
        self.sequence = sequence
        self.text = text
        self.unit_type = unit_type
        self.heading = heading

    @property
    def passage_sequences(
        self,
    ) -> list[int]:
        """Return supporting passage sequences."""

        return [
            self.sequence
        ]