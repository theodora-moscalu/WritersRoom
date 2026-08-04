from writersroom.processors.base_processor import (
    BaseProcessor,
)
from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


class ParagraphProcessor(BaseProcessor):
    """Splits text into paragraph source units."""

    def process(
        self,
        text: str,
    ) -> ProcessedDocument:
        """Convert raw text into paragraph source units."""

        units = []

        for sequence, paragraph in enumerate(
            text.split("\n\n"),
            start=1,
        ):

            paragraph = paragraph.strip()

            if paragraph:

                units.append(
                    SourceUnit(
                        sequence=sequence,
                        text=paragraph,
                        unit_type=(
                            SourceUnitType.PARAGRAPH
                        ),
                    )
                )

        return ProcessedDocument(
            source_units=units,
            metadata={
                "processor": "paragraph",
            },
        )