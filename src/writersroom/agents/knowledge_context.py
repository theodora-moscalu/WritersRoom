from writersroom.retrieval.knowledge_query import (
    KnowledgeQuery,
)


class KnowledgeContextBuilder:
    """Turns a writer's message into a block of relevant library knowledge."""

    def __init__(
        self,
        search_service,
        knowledge_repository,
        max_claims: int = 6,
        min_similarity: float = 0.4,
    ):
        self.search_service = search_service
        self.knowledge_repository = knowledge_repository
        self.max_claims = max_claims
        self.min_similarity = min_similarity

    def build(self, query_text: str, context_text: str = "") -> str:
        """Return a formatted knowledge block, or '' when nothing is relevant.

        `context_text` (e.g. the scene being worked on) steers the search when
        the message alone is too thin to retrieve on.
        """

        query_text = query_text.strip()
        context_text = context_text.strip()

        if not (query_text or context_text):
            return ""

        search_text = (
            f"{context_text[:1500]}\n\n{query_text}".strip()
            if context_text
            else query_text
        )

        results = self.search_service.search(
            KnowledgeQuery(
                text=search_text,
                max_results=self.max_claims * 3,
            )
        )

        relevant = [
            result
            for result in results
            if result.similarity >= self.min_similarity
        ][: self.max_claims]

        if not relevant:
            return ""

        lines = [
            "RELEVANT KNOWLEDGE FROM THE LIBRARY"
        ]

        for result in relevant:

            claim = result.claim

            kind = (
                "WORLD"
                if getattr(claim, "tier", "writing") == "general"
                else "CRAFT"
            )

            lines.append(
                f"[{claim.identity}] {kind} · "
                f"{claim.knowledge_domain.name} / "
                f"{claim.knowledge_level.name} "
                f"— from \"{self._source_name(claim)}\""
            )

            lines.append(
                f"  {claim.text}"
            )

            if claim.explanation:

                lines.append(
                    f"  Why: {claim.explanation}"
                )

        return "\n".join(lines)

    def _source_name(self, claim) -> str:
        """Resolve the knowledge source a claim came from, via its passage."""

        unknown = "unknown source"

        passage = self.knowledge_repository.get_passage(
            claim.passage_id
        )

        if passage is None:
            return unknown

        document = self.knowledge_repository.get_document(
            passage.document_id
        )

        if document is None:
            return unknown

        source = self.knowledge_repository.get_source(
            document.knowledge_source_id
        )

        return source.name if source else unknown
