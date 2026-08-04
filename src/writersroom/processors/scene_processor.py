import re

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


class SceneProcessor(BaseProcessor):
    """Splits screenplay text into scene source units."""

    _scene_heading = re.compile(
        r"^(INT\.|EXT\.|INT/EXT\.|I/E\.)",
        re.IGNORECASE,
    )

    def process(
        self,
        text: str,
    ) -> ProcessedDocument:
        """Convert screenplay text into scenes."""

        units = []

        heading = None

        body = []

        sequence = 1

        for line in text.splitlines():

            stripped = line.strip()

            if (
                self._scene_heading.match(
                    stripped
                )
            ):

                if heading is not None:

                    units.append(
                        SourceUnit(
                            sequence=sequence,
                            heading=heading,
                            text="\n".join(
                                body
                            ).strip(),
                            unit_type=(
                                SourceUnitType.SCENE
                            ),
                        )
                    )

                    sequence += 1

                    body = []

                heading = stripped

                continue

            if heading is not None:

                body.append(line)

        if heading is not None:

            units.append(
                SourceUnit(
                    sequence=sequence,
                    heading=heading,
                    text="\n".join(
                        body
                    ).strip(),
                    unit_type=(
                        SourceUnitType.SCENE
                    ),
                )
            )

        return ProcessedDocument(
            source_units=units,
            metadata={
                "processor": "scene",
            },
        )