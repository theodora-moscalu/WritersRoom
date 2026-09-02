from writersroom.extraction.extraction_granularity import (
    ExtractionGranularity,
)
from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
)
from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.processors.scene_builder import (
    SceneBuilder,
)


class ExtractionUnitSelector:
    """Selects extraction units from a processed document."""

    def __init__(self):

        self.scene_builder = (
            SceneBuilder()
        )

    def select(
        self,
        document: ProcessedDocument,
        granularity: ExtractionGranularity,
    ) -> list[ExtractionUnit]:
        """Return extraction units."""

        match granularity:

            case (
                ExtractionGranularity.SOURCE_UNIT
            ):
                return (
                    document.source_units
                )

            case (
                ExtractionGranularity.SCENE
            ):
                return (
                    self.scene_builder.build(
                        document
                    )
                )

            case (
                ExtractionGranularity.DOCUMENT
            ):
                raise NotImplementedError(
                    "Document extraction "
                    "not implemented."
                )

        raise ValueError(
            f"Unsupported extraction "
            f"granularity: "
            f"{granularity}"
        )