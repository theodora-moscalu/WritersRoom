from pathlib import Path

from writersroom.importers.importer_factory import (
    ImporterFactory,
)
from writersroom.processors.processor_factory import (
    ProcessorFactory,
)
from writersroom.processors.scene_builder import (
    SceneBuilder,
)


def main():

    print("=" * 70)
    print("SCENE ANALYSIS")
    print("=" * 70)

    pdf = (
        Path(__file__).parent
        / "data"
        / "Whiplash.pdf"
    )

    importer = (
        ImporterFactory.create(
            str(pdf)
        )
    )

    imported = (
        importer.import_document(
            str(pdf)
        )
    )

    processor = (
        ProcessorFactory.create(
            imported
        )
    )

    processed = (
        processor.process(
            imported.text
        )
    )

    builder = (
        SceneBuilder()
    )

    scenes = builder.build(
        processed
    )

    print()

    print(
        f"Source Units : {len(processed.source_units)}"
    )

    print(
        f"Scenes       : {len(scenes)}"
    )

    print()

    total_units = 0

    for index, scene in enumerate(
        scenes,
        start=1,
    ):

        units = len(
            scene.source_units
        )

        total_units += units

        print("-" * 70)

        print(
            f"Scene {index}"
        )

        print(
            f"Heading : {scene.heading}"
        )

        print(
            f"Source Units : {units}"
        )

        print(
            f"Passages : "
            f"{scene.first_sequence}"
            f" - "
            f"{scene.last_sequence}"
        )

    print()

    print("=" * 70)

    print(
        f"Total source units : {total_units}"
    )

    average = (
        total_units
        / len(scenes)
        if scenes
        else 0
    )

    print(
        f"Average source units per scene : "
        f"{average:.2f}"
    )


if __name__ == "__main__":
    main()