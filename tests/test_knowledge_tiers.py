from writersroom.database.database import Database
from writersroom.database.knowledge_repository import (
    KnowledgeRepository,
)
from writersroom.database.project_repository import (
    ProjectRepository,
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
from writersroom.services.claim_service import (
    ClaimService,
)
from writersroom.services.document_service import (
    DocumentService,
)
from writersroom.services.knowledge_source_service import (
    KnowledgeSourceService,
)
from writersroom.services.passage_service import (
    PassageService,
)


def seed(repository, project_id, source_name, tier, text, domain):
    KnowledgeSourceService(
        repository, project_id
    ).add_source(
        source_name,
        KnowledgeSourceType.BOOK,
        tier=tier,
    )
    DocumentService(repository, project_id).add_document(
        source_name, "doc"
    )
    PassageService(repository, project_id).add_passage(
        source_name, "doc", text
    )
    ClaimService(repository, project_id).add_claim(
        knowledge_source_name=source_name,
        document_name="doc",
        passage_sequence=1,
        text=text,
        knowledge_level=KnowledgeLevel.PRINCIPLE,
        knowledge_domain=domain,
    )


def main():
    print("Testing knowledge tiers...")

    database = Database(":memory:")
    repository = KnowledgeRepository(database)
    projects = ProjectRepository(database)

    wine = projects.create("The Wine Game")
    const = projects.create("Constantinople")

    seed(
        repository, None, "Save the Cat", "writing",
        "Every screenplay needs a catalyst.", KnowledgeDomain.STRUCTURE,
    )
    seed(
        repository, wine.identity, "Wine Fraud", "general",
        "Counterfeit bottles often have mismatched fill levels.",
        KnowledgeDomain.WORLD,
    )
    seed(
        repository, const.identity, "Byzantium", "general",
        "The Theodosian Walls stood for a thousand years.",
        KnowledgeDomain.WORLD,
    )

    wine_claims = {c.text for c in repository.list_claims(wine.identity)}
    const_claims = {c.text for c in repository.list_claims(const.identity)}
    shared_only = {c.text for c in repository.list_claims(None)}

    #
    # Writing tier is visible everywhere
    #

    assert "Every screenplay needs a catalyst." in wine_claims
    assert "Every screenplay needs a catalyst." in const_claims
    assert "Every screenplay needs a catalyst." in shared_only

    #
    # General tier is visible only to its own workspace
    #

    assert "mismatched fill levels." in " ".join(wine_claims)
    assert "mismatched fill levels." not in " ".join(const_claims)
    assert "Theodosian Walls" in " ".join(const_claims)
    assert "Theodosian Walls" not in " ".join(wine_claims)
    assert len(shared_only) == 1

    #
    # Tier tag is carried on the claim
    #

    tiers = {
        c.text: c.tier
        for c in repository.list_claims(wine.identity)
    }
    assert tiers["Every screenplay needs a catalyst."] == "writing"
    assert tiers[
        "Counterfeit bottles often have mismatched fill levels."
    ] == "general"

    #
    # A general source cannot be created without an open workspace
    #

    result = KnowledgeSourceService(
        repository, None
    ).add_source(
        "Homeless", KnowledgeSourceType.BOOK, tier="general"
    )
    assert not result.success

    print()
    print("Knowledge tier tests passed.")


if __name__ == "__main__":
    main()
