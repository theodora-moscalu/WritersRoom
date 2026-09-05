from writersroom.database.database import Database
from writersroom.database.knowledge_repository import (
    KnowledgeRepository,
)


def knowledge_repository() -> KnowledgeRepository:
    """Return a KnowledgeRepository backed by a fresh in-memory database."""

    return KnowledgeRepository(
        Database(":memory:")
    )
