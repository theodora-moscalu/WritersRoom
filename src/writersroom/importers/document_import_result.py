from dataclasses import dataclass


@dataclass
class DocumentImportResult:
    """Plain text extracted from an imported document."""

    filename: str
    text: str
    metadata: dict[str, str] | None = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}