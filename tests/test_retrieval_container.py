from writersroom.domains.workspace import (
    Workspace,
)
from writersroom.retrieval.retrieval_container import (
    RetrievalContainer,
)


def main():

    print(
        "Testing RetrievalContainer..."
    )

    workspace = (
        Workspace()
    )

    container = (
        RetrievalContainer(
            workspace
        )
    )

    assert (
        container.repository
        is not None
    )

    assert (
        container.provider
        is not None
    )

    assert (
        container.vector_store
        is not None
    )

    assert (
        container.indexer
        is not None
    )

    assert (
        container.retriever
        is not None
    )

    assert (
        container.search_service
        is not None
    )

    print()

    print(
        "RetrievalContainer tests passed."
    )


if __name__ == "__main__":
    main()