from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.document import (
    Document,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)


class ClaimRepository:
    """Provides read access to accepted knowledge."""

    def __init__(
        self,
        workspace,
    ):
        self.workspace = workspace

    def list_sources(
        self,
    ) -> list[KnowledgeSource]:
        """Return every knowledge source."""

        return (
            self.workspace.list_knowledge_sources()
        )

    def list_claims(
        self,
    ) -> list[Claim]:
        """Return every claim."""

        claims = []

        for source in (
            self.list_sources()
        ):

            claims.extend(
                self.list_source_claims(
                    source
                )
            )

        return claims

    def list_source_claims(
        self,
        source: KnowledgeSource,
    ) -> list[Claim]:
        """Return every claim in a knowledge source."""

        claims = []

        for document in (
            source.list_documents()
        ):

            claims.extend(
                self.list_document_claims(
                    document
                )
            )

        return claims

    def list_document_claims(
        self,
        document: Document,
    ) -> list[Claim]:
        """Return every claim in a document."""

        claims = []

        for passage in (
            document.list_passages()
        ):

            claims.extend(
                passage.list_claims()
            )

        return claims

    def find_claim(
        self,
        identity: str,
    ) -> Claim | None:
        """Find a claim by identity."""

        for claim in self.list_claims():

            if (
                claim.identity
                == identity
            ):
                return claim

        return None