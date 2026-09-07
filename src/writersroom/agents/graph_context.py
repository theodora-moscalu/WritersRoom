import re

from writersroom.graph.character_graph import (
    CharacterGraph,
)


class GraphContextBuilder:
    """Feeds the Showrunner the slice of the character graph that matters now."""

    def __init__(self, whole_graph_limit: int = 8):
        self.whole_graph_limit = whole_graph_limit

    def build(self, project, focus_text: str) -> str:
        """Return a CHARACTER GRAPH block for the characters in play, or ''."""

        graph = CharacterGraph.from_project(project)

        names = graph.characters()

        if not names:
            return ""

        focus = self._focus_characters(names, focus_text)

        if focus:
            return graph.render_block(focus)

        if len(names) <= self.whole_graph_limit:
            return graph.render_block([])

        return ""

    def _focus_characters(
        self,
        names: list[str],
        focus_text: str,
    ) -> list[str]:
        """Character names mentioned in the writer's message."""

        lowered = focus_text.lower()

        return [
            name
            for name in names
            if re.search(
                r"\b" + re.escape(name.lower()) + r"\b",
                lowered,
            )
        ]
