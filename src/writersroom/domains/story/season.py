class Season:
    """Represents a season of the series and the episodes it groups."""

    def __init__(
        self,
        number: int,
        title: str = "",
        logline: str = "",
        arc: str = "",
        question: str = "",
        theme: str = "",
        episode_titles: list[str] | None = None,
    ):
        self.number = number
        self.title = title
        self.logline = logline
        self.arc = arc
        self.question = question
        self.theme = theme
        self.episode_titles = episode_titles or []

    def add_episode_title(self, title: str):
        """Link an episode to this season by title."""

        if title not in self.episode_titles:
            self.episode_titles.append(title)

    def to_dict(self):
        """Convert the season to a dictionary."""

        return {
            "number": self.number,
            "title": self.title,
            "logline": self.logline,
            "arc": self.arc,
            "question": self.question,
            "theme": self.theme,
            "episode_titles": self.episode_titles,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Season from a dictionary."""

        return cls(
            number=data["number"],
            title=data.get("title", ""),
            logline=data.get("logline", ""),
            arc=data.get("arc", ""),
            question=data.get("question", ""),
            theme=data.get("theme", ""),
            episode_titles=data.get("episode_titles", []),
        )

    def __str__(self):
        if self.title:
            return f"Season {self.number}: {self.title}"

        return f"Season {self.number}"
