from enum import Enum


class ExtractionGranularity(Enum):
    """Defines the unit of source material used for extraction."""

    SOURCE_UNIT = "source_unit"

    SCENE = "scene"

    DOCUMENT = "document"