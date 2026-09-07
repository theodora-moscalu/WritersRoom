from writersroom.database.identity_generator import (
    IdentityGenerator,
)
from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.document import (
    Document,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)
from writersroom.domains.knowledge.passage import (
    Passage,
)
from writersroom.domains.knowledge.provenance import (
    Provenance,
)


class KnowledgeRepository:
    """The single owner of knowledge-library storage (ADR-019)."""

    def __init__(self, database):
        self.database = database
        self.identities = IdentityGenerator(database)

    def next_identity(self, prefix: IdentityPrefix) -> str:
        """Generate the next identity for a prefix."""

        return self.identities.next(prefix)

    #
    # Knowledge sources
    #

    def add_source(
        self,
        source: KnowledgeSource,
        tier: str = "writing",
        project_id: str | None = None,
    ):
        """Insert a knowledge source into a tier (writing is shared)."""

        source.tier = tier
        source.project_id = (
            project_id if tier == "general" else None
        )

        self.database.execute(
            "INSERT INTO knowledge_sources "
            "(identity, name, source_type, author, description, tier, project_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                source.identity,
                source.name,
                source.source_type.value,
                source.author,
                source.description,
                source.tier,
                source.project_id,
            ),
        )

    def get_source(self, identity: str) -> KnowledgeSource | None:
        """Return a knowledge source by identity."""

        row = self.database.query_one(
            "SELECT * FROM knowledge_sources WHERE identity = ?",
            (identity,),
        )

        return (
            self._source_from_row(row)
            if row
            else None
        )

    def get_source_by_name(
        self,
        name: str,
        project_id: str | None = None,
    ) -> KnowledgeSource | None:
        """Return a knowledge source by name, within the current scope."""

        row = self.database.query_one(
            "SELECT * FROM knowledge_sources "
            "WHERE lower(name) = lower(?) AND " + self._scope_clause(),
            (name, project_id),
        )

        return (
            self._source_from_row(row)
            if row
            else None
        )

    def list_sources(
        self,
        project_id: str | None = None,
        tier: str | None = None,
    ) -> list[KnowledgeSource]:
        """Return knowledge sources visible to the current scope."""

        if tier is not None:
            rows = self.database.query(
                "SELECT * FROM knowledge_sources "
                "WHERE tier = ? AND " + self._scope_clause()
                + " ORDER BY identity",
                (tier, project_id),
            )
        else:
            rows = self.database.query(
                "SELECT * FROM knowledge_sources "
                "WHERE " + self._scope_clause() + " ORDER BY identity",
                (project_id,),
            )

        return [
            self._source_from_row(row)
            for row in rows
        ]

    @staticmethod
    def _scope_clause(alias: str = "") -> str:
        """SQL predicate: shared writing tier plus one project's general tier.

        The bound parameter is the current project id (or None).
        """

        prefix = f"{alias}." if alias else ""

        return (
            f"({prefix}tier = 'writing' OR "
            f"({prefix}tier = 'general' AND {prefix}project_id = ?))"
        )

    def delete_source(self, identity: str):
        """Delete a knowledge source and everything beneath it."""

        self.database.execute(
            "DELETE FROM knowledge_sources WHERE identity = ?",
            (identity,),
        )

    def _source_from_row(self, row) -> KnowledgeSource:
        return KnowledgeSource(
            identity=row["identity"],
            name=row["name"],
            source_type=KnowledgeSourceType(
                row["source_type"]
            ),
            author=row["author"],
            description=row["description"],
            tier=row["tier"],
            project_id=row["project_id"],
        )

    #
    # Documents
    #

    def add_document(self, document: Document):
        """Insert a document."""

        self.database.execute(
            "INSERT INTO documents "
            "(identity, knowledge_source_id, name, description) "
            "VALUES (?, ?, ?, ?)",
            (
                document.identity,
                document.knowledge_source_id,
                document.name,
                document.description,
            ),
        )

    def get_document(self, identity: str) -> Document | None:
        """Return a document by identity."""

        row = self.database.query_one(
            "SELECT * FROM documents WHERE identity = ?",
            (identity,),
        )

        return (
            self._document_from_row(row)
            if row
            else None
        )

    def get_document_by_name(
        self,
        knowledge_source_id: str,
        name: str,
    ) -> Document | None:
        """Return a document within a source by name (case-insensitive)."""

        row = self.database.query_one(
            "SELECT * FROM documents "
            "WHERE knowledge_source_id = ? AND lower(name) = lower(?)",
            (knowledge_source_id, name),
        )

        return (
            self._document_from_row(row)
            if row
            else None
        )

    def list_documents(
        self,
        knowledge_source_id: str,
    ) -> list[Document]:
        """Return every document in a knowledge source."""

        return [
            self._document_from_row(row)
            for row in self.database.query(
                "SELECT * FROM documents "
                "WHERE knowledge_source_id = ? ORDER BY identity",
                (knowledge_source_id,),
            )
        ]

    def delete_document(self, identity: str):
        """Delete a document and everything beneath it."""

        self.database.execute(
            "DELETE FROM documents WHERE identity = ?",
            (identity,),
        )

    def _document_from_row(self, row) -> Document:
        return Document(
            identity=row["identity"],
            knowledge_source_id=row["knowledge_source_id"],
            name=row["name"],
            description=row["description"],
        )

    #
    # Passages
    #

    def add_passage(self, passage: Passage):
        """Insert a passage."""

        self.database.execute(
            "INSERT INTO passages "
            "(identity, document_id, sequence, text) "
            "VALUES (?, ?, ?, ?)",
            (
                passage.identity,
                passage.document_id,
                passage.sequence,
                passage.text,
            ),
        )

    def get_passage(self, identity: str) -> Passage | None:
        """Return a passage by identity."""

        row = self.database.query_one(
            "SELECT * FROM passages WHERE identity = ?",
            (identity,),
        )

        return (
            self._passage_from_row(row)
            if row
            else None
        )

    def get_passage_by_sequence(
        self,
        document_id: str,
        sequence: int,
    ) -> Passage | None:
        """Return a passage within a document by sequence."""

        row = self.database.query_one(
            "SELECT * FROM passages "
            "WHERE document_id = ? AND sequence = ?",
            (document_id, sequence),
        )

        return (
            self._passage_from_row(row)
            if row
            else None
        )

    def list_passages(
        self,
        document_id: str,
    ) -> list[Passage]:
        """Return every passage in a document."""

        return [
            self._passage_from_row(row)
            for row in self.database.query(
                "SELECT * FROM passages "
                "WHERE document_id = ? ORDER BY sequence",
                (document_id,),
            )
        ]

    def next_passage_sequence(
        self,
        document_id: str,
    ) -> int:
        """Return the next available passage sequence for a document."""

        row = self.database.query_one(
            "SELECT MAX(sequence) AS highest FROM passages "
            "WHERE document_id = ?",
            (document_id,),
        )

        return (
            row["highest"] or 0
        ) + 1

    def delete_passage(self, identity: str):
        """Delete a passage and everything beneath it."""

        self.database.execute(
            "DELETE FROM passages WHERE identity = ?",
            (identity,),
        )

    def _passage_from_row(self, row) -> Passage:
        return Passage(
            identity=row["identity"],
            document_id=row["document_id"],
            sequence=row["sequence"],
            text=row["text"],
        )

    #
    # Claims
    #

    def add_claim(self, claim: Claim):
        """Insert a claim and its provenance."""

        with self.database.transaction() as connection:

            connection.execute(
                "INSERT INTO claims "
                "(identity, passage_id, text, "
                "knowledge_level, knowledge_domain, explanation) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    claim.identity,
                    claim.passage_id,
                    claim.text,
                    claim.knowledge_level.value,
                    claim.knowledge_domain.value,
                    claim.explanation,
                ),
            )

            for item in claim.provenance:

                connection.execute(
                    "INSERT INTO provenance "
                    "(identity, claim_id, source_document_id, "
                    "passage_id, confidence, reviewed) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        item.identity,
                        item.claim_id,
                        item.source_document_id,
                        item.passage_id,
                        item.confidence,
                        int(item.reviewed),
                    ),
                )

    def get_claim(self, identity: str) -> Claim | None:
        """Return a claim by identity."""

        row = self.database.query_one(
            "SELECT * FROM claims WHERE identity = ?",
            (identity,),
        )

        return (
            self._claim_from_row(row)
            if row
            else None
        )

    def list_claims(
        self,
        project_id: str | None = None,
    ) -> list[Claim]:
        """Return claims visible to the current scope, tagged with their tier."""

        rows = self.database.query(
            "SELECT c.*, ks.tier AS source_tier "
            "FROM claims c "
            "JOIN passages p ON p.identity = c.passage_id "
            "JOIN documents d ON d.identity = p.document_id "
            "JOIN knowledge_sources ks ON ks.identity = d.knowledge_source_id "
            "WHERE " + self._scope_clause("ks")
            + " ORDER BY c.identity",
            (project_id,),
        )

        claims = []

        for row in rows:
            claim = self._claim_from_row(row)
            claim.tier = row["source_tier"]
            claims.append(claim)

        return claims

    def list_claims_for_passage(
        self,
        passage_id: str,
    ) -> list[Claim]:
        """Return every claim attached to a passage."""

        return [
            self._claim_from_row(row)
            for row in self.database.query(
                "SELECT * FROM claims "
                "WHERE passage_id = ? ORDER BY identity",
                (passage_id,),
            )
        ]

    def delete_claim(self, identity: str):
        """Delete a claim and its provenance and embedding."""

        self.database.execute(
            "DELETE FROM claims WHERE identity = ?",
            (identity,),
        )

    def _claim_from_row(self, row) -> Claim:
        claim = Claim(
            identity=row["identity"],
            passage_id=row["passage_id"],
            text=row["text"],
            knowledge_level=KnowledgeLevel(
                row["knowledge_level"]
            ),
            knowledge_domain=KnowledgeDomain(
                row["knowledge_domain"]
            ),
            explanation=row["explanation"],
        )

        for item in self.database.query(
            "SELECT * FROM provenance "
            "WHERE claim_id = ? ORDER BY identity",
            (row["identity"],),
        ):

            claim.add_provenance(
                Provenance(
                    identity=item["identity"],
                    claim_id=item["claim_id"],
                    source_document_id=item["source_document_id"],
                    passage_id=item["passage_id"],
                    confidence=item["confidence"],
                    reviewed=bool(item["reviewed"]),
                )
            )

        return claim
