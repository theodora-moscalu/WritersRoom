from writersroom.domains.workspace import Workspace


def main():
    print("Testing Workspace...")

    workspace = Workspace()

    assert workspace.projects == []

    workspace.add_project(
        type("P", (), {"title": "The Wine Game"})
    )

    assert workspace.projects == ["The Wine Game"]

    workspace.remove_project("The Wine Game")

    assert workspace.projects == []

    print("Workspace tests passed.")


if __name__ == "__main__":
    main()
