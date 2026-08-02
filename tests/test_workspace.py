from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)
from writersroom.domains.workspace import Workspace


def main():
    print("Testing Workspace...")

    workspace = Workspace()

    assert workspace.projects == []
    assert workspace.knowledge_sources == []
    assert workspace.personal_knowledge == []

    assert (
        workspace.generate_identity(
            IdentityPrefix.KNOWLEDGE_SOURCE
        )
        == "KS000001"
    )

    assert (
        workspace.generate_identity(
            IdentityPrefix.KNOWLEDGE_SOURCE
        )
        == "KS000002"
    )

    assert (
        workspace.generate_identity(
            IdentityPrefix.DOCUMENT
        )
        == "DOC000001"
    )

    workspace.save()

    loaded = Workspace.load()

    assert loaded.identity_counters == {
        "KS": 2,
        "DOC": 1,
    }

    assert (
        loaded.generate_identity(
            IdentityPrefix.KNOWLEDGE_SOURCE
        )
        == "KS000003"
    )

    assert (
        loaded.generate_identity(
            IdentityPrefix.DOCUMENT
        )
        == "DOC000002"
    )

    print("Workspace tests passed.")


if __name__ == "__main__":
    main()