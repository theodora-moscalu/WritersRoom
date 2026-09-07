from writersroom.graph.character_graph import (
    CharacterGraph,
)


class GraphCommands:
    """Handles `graph` commands — the character relationship graph."""

    def __init__(self, project):
        self.project = project

    def handle(self, args: list[str]):
        """Handle graph commands."""

        graph = CharacterGraph.from_project(self.project)

        if not graph.characters():
            print("\nThis workspace has no characters yet.\n")
            return

        if not args:
            self._overview(graph)
            return

        action = args[0].lower()

        if action == "isolated":
            self._isolated(graph)
            return

        if action == "between" and len(args) >= 3:
            self._between(graph, args[1], " ".join(args[2:]))
            return

        self._character(graph, " ".join(args))

    def _overview(self, graph: CharacterGraph):
        print()
        print("Character Graph")
        print("--------------")

        block = graph.render_block([])
        print(block.replace("CHARACTER GRAPH\n", "") or "  (no relationships)")

        isolated = graph.isolated()
        if isolated:
            print()
            print("Isolated: " + ", ".join(isolated))

        connected = graph.most_connected()
        if connected:
            print()
            print(
                "Most connected: "
                + ", ".join(f"{name} ({count})" for name, count in connected)
            )

        print()

    def _isolated(self, graph: CharacterGraph):
        isolated = graph.isolated()

        print()
        if isolated:
            print("Characters with no relationships:")
            for name in isolated:
                print(f"  {name}")
        else:
            print("Every character has at least one relationship.")
        print()

    def _character(self, graph: CharacterGraph, name: str):
        resolved = graph.resolve(name)

        print()
        if resolved is None:
            print(f"No character called '{name}'.")
            print()
            return

        print(resolved)
        print("-" * len(resolved))

        edges = graph.neighbours(resolved)

        if not edges:
            print("  (no relationships)")
        else:
            for other, kind, direction in edges:
                arrow = "->" if direction == "->" else "<-"
                print(f"  {arrow} {other} ({kind})")

        print()

    def _between(self, graph: CharacterGraph, source: str, target: str):
        path = graph.path_between(source, target)

        print()
        if path is None:
            print(f"No connection between '{source}' and '{target}'.")
        else:
            print(" -> ".join(path))
        print()

    def print_help(self):
        print()
        print("Graph commands")
        print("--------------")
        print("graph                    Overview of the character web")
        print("graph <name>             One character's relationships")
        print("graph isolated           Characters with no relationships")
        print("graph between <a> <b>    Shortest connection between two characters")
        print()
