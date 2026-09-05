import sqlite3
from contextlib import contextmanager
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS knowledge_sources (
    identity TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    author TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS documents (
    identity TEXT PRIMARY KEY,
    knowledge_source_id TEXT NOT NULL
        REFERENCES knowledge_sources(identity) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS passages (
    identity TEXT PRIMARY KEY,
    document_id TEXT NOT NULL
        REFERENCES documents(identity) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    text TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS claims (
    identity TEXT PRIMARY KEY,
    passage_id TEXT NOT NULL
        REFERENCES passages(identity) ON DELETE CASCADE,
    text TEXT NOT NULL,
    knowledge_level TEXT NOT NULL,
    knowledge_domain TEXT NOT NULL,
    explanation TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS provenance (
    identity TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL
        REFERENCES claims(identity) ON DELETE CASCADE,
    source_document_id TEXT NOT NULL,
    passage_id TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    reviewed INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS embeddings (
    claim_id TEXT PRIMARY KEY
        REFERENCES claims(identity) ON DELETE CASCADE,
    model TEXT NOT NULL,
    dimensions INTEGER NOT NULL,
    vector BLOB NOT NULL,
    text_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS identity_counters (
    prefix TEXT PRIMARY KEY,
    value INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_documents_source
    ON documents(knowledge_source_id);
CREATE INDEX IF NOT EXISTS idx_passages_document
    ON passages(document_id);
CREATE INDEX IF NOT EXISTS idx_claims_passage
    ON claims(passage_id);
CREATE INDEX IF NOT EXISTS idx_provenance_claim
    ON provenance(claim_id);
"""


class Database:
    """Owns the SQLite connection for the knowledge library."""

    DEFAULT_PATH = Path("workspace") / "knowledge.db"

    def __init__(self, path=None):
        if path is None:
            path = self.DEFAULT_PATH

        self.path = path

        if isinstance(path, Path):
            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        self._connection = sqlite3.connect(
            path,
            check_same_thread=False,
        )

        self._connection.row_factory = sqlite3.Row

        self._connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        self._connection.executescript(SCHEMA)

        self._connection.commit()

    def execute(self, sql, params=()):
        """Run a write statement and commit."""

        cursor = self._connection.execute(
            sql,
            params,
        )

        self._connection.commit()

        return cursor

    def query(self, sql, params=()):
        """Return every row for a query."""

        return self._connection.execute(
            sql,
            params,
        ).fetchall()

    def query_one(self, sql, params=()):
        """Return the first row for a query, or None."""

        return self._connection.execute(
            sql,
            params,
        ).fetchone()

    @contextmanager
    def transaction(self):
        """Group several statements into one commit."""

        try:
            yield self._connection
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise

    def close(self):
        """Close the connection."""

        self._connection.close()
