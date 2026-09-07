class ProjectContextBuilder:
    """Turns the current project's story data into a compact context block."""

    def build(self, project) -> str:
        """Return a formatted project block, or '' when the project is empty."""

        sections = []

        if project.characters:
            sections.append(
                "Characters:\n"
                + "\n".join(
                    self._character_line(character)
                    for character in project.characters
                )
            )

        if project.character_relationships:
            sections.append(
                "Relationships:\n"
                + "\n".join(
                    f"  {relationship}"
                    for relationship in project.character_relationships
                )
            )

        if project.locations:
            sections.append(
                "Locations:\n"
                + "\n".join(
                    f"  {location.name}"
                    for location in project.locations
                )
            )

        if project.seasons:
            sections.append(
                "Seasons:\n"
                + "\n".join(
                    self._season_block(season, project)
                    for season in project.seasons
                )
            )

        if project.episodes:
            sections.append(
                "Episodes:\n"
                + "\n".join(
                    self._episode_line(episode)
                    for episode in project.episodes
                )
            )

        if project.notes:
            sections.append(
                "Notes:\n"
                + "\n".join(
                    f"  {note.title}: {note.content}"
                    for note in project.notes
                )
            )

        if not sections:
            return ""

        return (
            f"CURRENT PROJECT: {project.title}\n\n"
            + "\n\n".join(sections)
        )

    def _character_line(self, character) -> str:
        line = f"  {character.name}"

        if character.description:
            line += f" — {character.description}"

        detail = ", ".join(
            f"{label}: {value}"
            for label, value in (
                ("want", character.want),
                ("need", character.need),
                ("flaw", character.flaw),
                ("arc", character.arc),
            )
            if value
        )

        if detail:
            line += f"\n      ({detail})"

        return line

    def _season_block(self, season, project) -> str:
        header = f"  {season}"

        parts = [
            f"{label}: {value}"
            for label, value in (
                ("question", season.question),
                ("arc", season.arc),
                ("theme", season.theme),
            )
            if value
        ]

        if parts:
            header += "\n      " + " | ".join(parts)

        for title in season.episode_titles:
            header += f"\n      - {title}"

        return header

    def _episode_line(self, episode) -> str:
        line = f"  {episode.title} [{episode.status.value}]"

        if episode.logline:
            line += f" — {episode.logline}"

        stories = ", ".join(
            f"{label}: {value}"
            for label, value in (
                ("A", episode.a_story),
                ("B", episode.b_story),
            )
            if value
        )

        if stories:
            line += f"\n      ({stories})"

        return line
