from collections.abc import Iterable


class KnowledgeNormalizer:
    """Normalizes LLM output before parsing."""

    _aliases = {
        "LEVEL:": (
            "LEVEL",
            "LEVEL:",
        ),
        "DOMAIN:": (
            "DOMAIN",
            "DOMAIN:",
        ),
        "IMPORTANCE:": (
            "IMPORT",
            "IMPORTANCE",
            "IMPORTANCE:",
        ),
        "TEXT:": (
            "TEXT",
            "TEXT:",
        ),
        "EXPLANATION:": (
            "EXPLANATION",
            "EXPLANATION:",
        ),
    }

    _enum_values = {
        "LEVEL:": (
            "OBSERVATION",
            "TECHNIQUE",
            "PRINCIPLE",
        ),
        "DOMAIN:": (
            "STRUCTURE",
            "CHARACTER",
            "SCENE",
            "CONFLICT",
            "DIALOGUE",
            "EMOTION",
            "THEME",
            "VISUAL",
            "WORLD",
            "WRITING",
        ),
        "IMPORTANCE:": (
            "LOW",
            "MEDIUM",
            "HIGH",
        ),
    }

    def __init__(self):

        self._lookup = {}

        for canonical, aliases in (
            self._aliases.items()
        ):
            self._register(
                canonical,
                aliases,
            )

    def normalize(
        self,
        text: str,
    ) -> str:
        """Normalize LLM output."""

        lines = []

        current_header = None

        for line in text.splitlines():

            stripped = line.strip()

            replacement = self._lookup.get(
                stripped.upper()
            )

            if replacement:

                stripped = replacement
                current_header = replacement

            elif current_header in self._enum_values:

                stripped = self._normalize_enum(
                    current_header,
                    stripped,
                )

            lines.append(
                stripped
            )

        return "\n".join(
            lines
        )

    def _normalize_enum(
        self,
        header: str,
        value: str,
    ) -> str:
        """Normalize enum values using unique prefix matching."""

        upper = value.upper()

        matches = [
            candidate
            for candidate in self._enum_values[
                header
            ]
            if candidate.startswith(
                upper
            )
        ]

        if len(matches) == 1:

            return matches[0]

        return value

    def _register(
        self,
        canonical: str,
        aliases: Iterable[str],
    ):

        for alias in aliases:

            self._lookup[
                alias.upper()
            ] = canonical