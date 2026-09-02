from writersroom.processors.processed_document import (
    ProcessedDocument,
)
from writersroom.processors.scene import (
    Scene,
)
from writersroom.processors.source_unit_type import (
    SourceUnitType,
)


class SceneBuilder:
    """Builds scenes from processed source units."""

    def build(
        self,
        document: ProcessedDocument,
    ) -> list[Scene]:

        scenes: list[Scene] = []

        current = []

        heading = None

        for unit in document.source_units:

            if (
                unit.unit_type
                == SourceUnitType.SCENE
            ):

                if current:

                    scenes.append(
                        Scene(
                            heading=heading
                            or "Scene",
                            source_units=current,
                        )
                    )

                current = [unit]

                heading = unit.heading

            else:

                current.append(unit)

        if current:

            scenes.append(
                Scene(
                    heading=heading
                    or "Scene",
                    source_units=current,
                )
            )

        return scenes