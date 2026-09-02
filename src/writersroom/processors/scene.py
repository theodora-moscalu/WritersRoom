from writersroom.processors.source_unit import (
    SourceUnit,
)


class Scene:
    """Represents a screenplay scene."""

    def __init__(
        self,
        heading: str,
        source_units: list[SourceUnit],
    ):
        self.heading = heading
        self.source_units = source_units

    @property
    def text(self) -> str:
        """Return the complete scene text."""

        return "\n\n".join(
            unit.text
            for unit in self.source_units
        )

    @property
    def first_sequence(
        self,
    ) -> int:
        """Return the first source unit sequence."""

        return self.source_units[
            0
        ].sequence

    @property
    def last_sequence(
        self,
    ) -> int:
        """Return the last source unit sequence."""

        return self.source_units[
            -1
        ].sequence

    @property
    def passage_sequences(
        self,
    ) -> list[int]:
        """Return supporting passage sequences."""

        return [
            unit.sequence
            for unit in self.source_units
        ]