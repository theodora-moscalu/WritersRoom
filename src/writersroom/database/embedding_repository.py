import hashlib
from array import array

from writersroom.domains.knowledge.embedding import (
    Embedding,
)


def text_hash(text: str) -> str:
    """Return a stable hash of claim text."""

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


class EmbeddingRepository:
    """Persists claim embeddings alongside the knowledge library."""

    def __init__(self, database):
        self.database = database

    def get(self, claim_id: str) -> Embedding | None:
        """Return the stored embedding for a claim, or None."""

        row = self.database.query_one(
            "SELECT model, vector FROM embeddings WHERE claim_id = ?",
            (claim_id,),
        )

        if row is None:
            return None

        vector = array("f")
        vector.frombytes(row["vector"])

        return Embedding(
            model=row["model"],
            vector=list(vector),
        )

    def get_text_hash(self, claim_id: str) -> str | None:
        """Return the text hash the stored embedding was built from."""

        row = self.database.query_one(
            "SELECT text_hash FROM embeddings WHERE claim_id = ?",
            (claim_id,),
        )

        return row["text_hash"] if row else None

    def upsert(
        self,
        claim_id: str,
        text: str,
        embedding: Embedding,
    ):
        """Store or replace the embedding for a claim."""

        blob = array(
            "f",
            embedding.vector,
        ).tobytes()

        self.database.execute(
            "INSERT INTO embeddings "
            "(claim_id, model, dimensions, vector, text_hash) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(claim_id) DO UPDATE SET "
            "model = excluded.model, "
            "dimensions = excluded.dimensions, "
            "vector = excluded.vector, "
            "text_hash = excluded.text_hash",
            (
                claim_id,
                embedding.model,
                embedding.dimensions,
                blob,
                text_hash(text),
            ),
        )

    def delete(self, claim_id: str):
        """Remove the embedding for a claim."""

        self.database.execute(
            "DELETE FROM embeddings WHERE claim_id = ?",
            (claim_id,),
        )
