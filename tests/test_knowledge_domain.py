from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.domains.knowledge.citation import (
    Citation,
)
from writersroom.domains.knowledge.claim import (
    Claim,
)
from writersroom.domains.knowledge.document import (
    Document,
)
from writersroom.domains.knowledge.knowledge_library import (
    KnowledgeLibrary,
)
from writersroom.domains.knowledge.knowledge_source import (
    KnowledgeSource,
)
from writersroom.domains.knowledge.passage import (
    Passage,
)
from writersroom.domains.workspace import Workspace


def main():
    print("Testing Knowledge Domain...")

    workspace = Workspace()

    library = KnowledgeLibrary()

    source = KnowledgeSource(
        identity=workspace.generate_identity(
            IdentityPrefix.KNOWLEDGE_SOURCE
        ),
        name="Story",
        source_type=KnowledgeSourceType.BOOK,
        author="Robert McKee",
        description="Classic screenwriting book.",
    )

    document = Document(
        identity=workspace.generate_identity(
            IdentityPrefix.DOCUMENT
        ),
        knowledge_source_id=source.identity,
        name="Chapter 1",
    )

    passage = Passage(
        identity=workspace.generate_identity(
            IdentityPrefix.PASSAGE
        ),
        document_id=document.identity,
        title="Opening Image",
        text=(
            "The opening image establishes "
            "the tone of the story."
        ),
    )

    claim = Claim(
        identity=workspace.generate_identity(
            IdentityPrefix.CLAIM
        ),
        passage_id=passage.identity,
        text=(
            "The opening image should establish "
            "the story's tone."
        ),
        explanation=(
            "It prepares the audience for the "
            "journey ahead."
        ),
        tags=[
            "structure",
            "opening",
        ],
    )

    citation = Citation(
        identity=workspace.generate_identity(
            IdentityPrefix.CITATION
        ),
        claim_id=claim.identity,
        source_document_id=document.identity,
        location="Chapter 1",
        excerpt=(
            "The opening image establishes "
            "the tone of the story."
        ),
    )

    claim.citations.append(
        citation
    )

    passage.claims.append(
        claim
    )

    document.passages.append(
        passage
    )

    source.documents.append(
        document
    )

    library.add_source(
        source
    )

    assert len(library) == 1

    assert (
        library.find_source(
            source.identity
        )
        is source
    )

    data = library.to_dict()

    loaded_library = (
        KnowledgeLibrary.from_dict(data)
    )

    assert len(loaded_library) == 1

    loaded_source = (
        loaded_library.find_source(
            source.identity
        )
    )

    assert loaded_source is not None

    loaded_document = (
        loaded_source.documents[0]
    )

    loaded_passage = (
        loaded_document.passages[0]
    )

    loaded_claim = (
        loaded_passage.claims[0]
    )

    loaded_citation = (
        loaded_claim.citations[0]
    )

    assert (
        loaded_source.name
        == "Story"
    )

    assert (
        loaded_document.name
        == "Chapter 1"
    )

    assert (
        loaded_passage.title
        == "Opening Image"
    )

    assert (
        loaded_claim.text
        == (
            "The opening image should "
            "establish the story's tone."
        )
    )

    assert (
        loaded_citation.location
        == "Chapter 1"
    )

    print(
        "Knowledge Domain tests passed."
    )


if __name__ == "__main__":
    main()