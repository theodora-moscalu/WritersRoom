import os

from writersroom.database.database import Database
from writersroom.database.knowledge_repository import (
    KnowledgeRepository,
)
from writersroom.database.project_repository import (
    ProjectRepository,
)


def knowledge_repository() -> KnowledgeRepository:
    """Return a KnowledgeRepository backed by a fresh in-memory database."""

    return KnowledgeRepository(
        Database(":memory:")
    )


def project_repository(database=None) -> ProjectRepository:
    """Return a ProjectRepository, sharing a database when one is given."""

    return ProjectRepository(
        database or Database(":memory:")
    )


def limit_source_units(processed):
    """Cap a ProcessedDocument to the first few units for cheap end-to-end runs.

    Extraction makes one LLM call per source unit, so the end-to-end tests
    process only the first 3 by default. Set WRITERSROOM_E2E_SCENE_LIMIT=0
    to run the whole document.
    """

    limit = int(
        os.getenv("WRITERSROOM_E2E_SCENE_LIMIT", "3")
    )

    if limit > 0:
        processed.source_units = (
            processed.source_units[:limit]
        )

    return processed
