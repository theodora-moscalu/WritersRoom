from pathlib import Path

from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.workspace import (
    Workspace,
)
from writersroom.importers.importer_factory import (
    ImporterFactory,
)
from writersroom.processors.processor_factory import (
    ProcessorFactory,
)
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_pipeline_service import (
    KnowledgePipelineService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)


def main():

    print("=" * 60)
    print("WRITERSROOM END-TO-END PIPELINE")
    print("=" * 60)

    workspace = Workspace()

    knowledge_sources = (
        KnowledgeSourceService(
            workspace
        )
    )

    documents = (
        DocumentService(
            workspace
        )
    )

    passages = (
        PassageService(
            workspace
        )
    )

    claims = (
        ClaimService(
            workspace
        )
    )

    pipeline = (
        KnowledgePipelineService(
            workspace
        )
    )

    pdf = (
        Path(__file__).parent
        / "data"
        / "Whiplash.pdf"
    )

    print()
    print("Importing PDF...")

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

    print("✓ Imported")

    print()
    print("Processing...")

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

    print(
        f"✓ Created {len(processed.source_units)} "
        "SourceUnits"
    )

    print()
    print("Creating knowledge source...")

    knowledge_sources.add_source(
        name="Whiplash",
        source_type=(
            KnowledgeSourceType.SCREENPLAY
        ),
    )

    documents.add_document(
        knowledge_source_name="Whiplash",
        name="Whiplash.pdf",
    )

    for unit in processed.source_units:

        passages.add_passage(
            knowledge_source_name="Whiplash",
            document_name="Whiplash.pdf",
            text=unit.text,
        )

    print("✓ Stored document")

    print()
    print("Extracting knowledge...")

    review = pipeline.process(
        knowledge_source_name="Whiplash",
        document_name="Whiplash.pdf",
        processed_document=processed,
    )

    print(
        f"✓ Accepted "
        f"{len(review.accepted_items)} claims"
    )

    print()
    print("=" * 60)
    print("FIRST THREE SOURCE UNITS")
    print("=" * 60)

    for unit in processed.source_units[:3]:

        result = (
            claims.list_claims(
                "Whiplash",
                "Whiplash.pdf",
                unit.sequence,
            )
        )

        print()

        print("-" * 60)

        print(
            f"Source Unit {unit.sequence}"
        )

        if unit.heading:

            print()
            print("Heading:")
            print(unit.heading)

        print()
        print("Text:")
        print(unit.text[:300])

        print()

        if result.success:

            for claim in result.data:

                print("Claim:")
                print(claim.text)
                print()

        else:

            print("No claims stored.")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(
        f"Source Units : "
        f"{len(processed.source_units)}"
    )

    print(
        f"Accepted     : "
        f"{len(review.accepted_items)}"
    )

    print(
        f"Rejected     : "
        f"{len(review.rejected_items)}"
    )

    assert (
        len(review.accepted_items)
        == len(processed.source_units)
    )

    print()
    print("End-to-end pipeline passed.")


if __name__ == "__main__":
    main()