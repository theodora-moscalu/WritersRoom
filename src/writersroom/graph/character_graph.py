import networkx as nx


class CharacterGraph:
    """A derived view of a project's characters and their relationships."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph

    #
    # Construction
    #

    @classmethod
    def from_project(cls, project) -> "CharacterGraph":
        """Build the graph from the project's current story data."""

        graph = nx.MultiDiGraph()

        for character in project.characters:
            graph.add_node(
                character.name,
                description=character.description,
                want=character.want,
                need=character.need,
                flaw=character.flaw,
                arc=character.arc,
            )

        for relationship in project.character_relationships:

            for name in (relationship.source, relationship.target):
                if name not in graph:
                    graph.add_node(name)

            graph.add_edge(
                relationship.source,
                relationship.target,
                key=relationship.relationship.value,
                type=relationship.relationship.value,
                history=[
                    str(beat) for beat in relationship.history
                ],
            )

        return cls(graph)

    #
    # Queries
    #

    def characters(self) -> list[str]:
        return list(self.graph.nodes)

    def resolve(self, name: str) -> str | None:
        """Match a name case-insensitively to a graph node."""

        lowered = name.strip().lower()

        for node in self.graph.nodes:
            if node.lower() == lowered:
                return node

        return None

    def neighbours(self, name: str) -> list[tuple[str, str, str]]:
        """Return (other, type, direction) for every edge touching a character."""

        node = self.resolve(name)

        if node is None:
            return []

        edges = []

        for _, target, data in self.graph.out_edges(node, data=True):
            edges.append((target, data["type"], "->"))

        for source, _, data in self.graph.in_edges(node, data=True):
            edges.append((source, data["type"], "<-"))

        return edges

    def isolated(self) -> list[str]:
        """Characters with no relationships at all."""

        return sorted(
            node
            for node in self.graph.nodes
            if self.graph.degree(node) == 0
        )

    def most_connected(self, limit: int = 3) -> list[tuple[str, int]]:
        ranked = sorted(
            self.graph.degree,
            key=lambda pair: pair[1],
            reverse=True,
        )

        return [pair for pair in ranked[:limit] if pair[1] > 0]

    def path_between(self, source: str, target: str) -> list[str] | None:
        start = self.resolve(source)
        end = self.resolve(target)

        if start is None or end is None:
            return None

        undirected = self.graph.to_undirected(as_view=True)

        try:
            return nx.shortest_path(undirected, start, end)
        except nx.NetworkXNoPath:
            return None

    def relationship_summary(self, source: str, target: str) -> list[str]:
        start = self.resolve(source)
        end = self.resolve(target)

        if start is None or end is None:
            return []

        summaries = []

        for a, b in ((start, end), (end, start)):
            if self.graph.has_edge(a, b):
                for data in self.graph[a][b].values():
                    text = f"{a} -> {b}: {data['type']}"
                    if data["history"]:
                        text += " (" + "; ".join(data["history"]) + ")"
                    summaries.append(text)

        return summaries

    #
    # Rendering
    #

    def ego_names(self, names: list[str], radius: int = 1) -> list[str]:
        """The named characters plus everyone within `radius` hops."""

        resolved = [
            node
            for node in (self.resolve(name) for name in names)
            if node is not None
        ]

        if not resolved:
            return []

        undirected = self.graph.to_undirected(as_view=True)
        reached = set(resolved)

        for node in resolved:
            reached.update(
                nx.ego_graph(undirected, node, radius=radius).nodes
            )

        return sorted(reached)

    def render_block(self, names: list[str]) -> str:
        """Render the relevant sub-graph as compact text for a prompt."""

        if names:
            scope = set(self.ego_names(names))
        else:
            scope = set(self.graph.nodes)

        if not scope:
            return ""

        lines = []

        for source, target, data in sorted(
            self.graph.edges(data=True)
        ):
            if source not in scope or target not in scope:
                continue

            line = f"  {source} --{data['type']}--> {target}"

            if data["history"]:
                line += "  (" + "; ".join(data["history"]) + ")"

            lines.append(line)

        if not lines:
            return ""

        return "CHARACTER GRAPH\n" + "\n".join(lines)

    def to_dot(self) -> str:
        """Render the whole graph as Graphviz DOT."""

        lines = ["digraph characters {", "  rankdir=LR;", "  node [shape=box];"]

        for node in self.graph.nodes:
            safe = node.replace('"', "'")
            lines.append(f'  "{safe}";')

        for source, target, data in self.graph.edges(data=True):
            s = source.replace('"', "'")
            t = target.replace('"', "'")
            lines.append(f'  "{s}" -> "{t}" [label="{data["type"]}"];')

        lines.append("}")

        return "\n".join(lines)
