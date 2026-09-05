class ProjectContextBuilder:
    """Turns the current project's story data into a compact context block."""

    def build(self, project) -> str:
        """Return a formatted project block, or '' when the project is empty."""

        sections = []

        if project.characters:

            sections.append(
                "Characters:\n"
                + "\n".join(
                    f"  {character.name}"
                    + (
                        f" — {character.description}"
                        if character.description
                        else ""
                    )
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

        if project.episodes:

            sections.append(
                "Episodes:\n"
                + "\n".join(
                    f"  {episode.title} [{episode.status.value}]"
                    + (
                        f" — {episode.logline}"
                        if episode.logline
                        else ""
                    )
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
