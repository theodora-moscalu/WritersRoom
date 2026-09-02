from typing import Protocol


class ExtractionUnit(Protocol):
    """Represents a unit of source material."""

    @property
    def text(self) -> str:
        ...

    @property
    def heading(self) -> str | None:
        ...

    @property
    def passage_sequences(
        self,
    ) -> list[int]:
        """Return the supporting passage sequences."""
        ...