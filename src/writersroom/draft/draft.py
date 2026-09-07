from dataclasses import dataclass
from dataclasses import field


@dataclass
class DraftScene:
    """One scene of the current script."""

    number: int
    heading: str
    text: str = ""
    characters: list[str] = field(default_factory=list)
    synopsis: str = ""

    def one_line(self) -> str:
        """A single-line summary for the outline."""

        if self.synopsis:
            detail = self.synopsis
        else:
            detail = next(
                (
                    line.strip()
                    for line in self.text.splitlines()
                    if line.strip()
                    and line.strip() != line.strip().upper()
                ),
                "",
            )

        detail = detail[:100]

        return (
            f"{self.number}. {self.heading}"
            + (f" — {detail}" if detail else "")
        )


@dataclass
class Draft:
    """A live view of the writer's current script — never stored."""

    scenes: list[DraftScene] = field(default_factory=list)
    source_path: str = ""
    format: str = ""
    read_at: str = ""
    changed_scenes: list[int] = field(default_factory=list)

    def latest_change(self) -> DraftScene | None:
        """The scene the writer most recently edited, if the diff caught one."""

        if not self.changed_scenes:
            return None

        return self.scene(self.changed_scenes[-1])

    def scene(self, number: int) -> DraftScene | None:
        for scene in self.scenes:
            if scene.number == number:
                return scene

        return None

    def last_scene(self) -> DraftScene | None:
        return self.scenes[-1] if self.scenes else None

    def preceding(self, number: int) -> list[DraftScene]:
        return [
            scene
            for scene in self.scenes
            if scene.number < number
        ]

    def scenes_with_character(self, name: str) -> list[DraftScene]:
        lowered = name.strip().lower()

        return [
            scene
            for scene in self.scenes
            if any(
                character.lower() == lowered
                for character in scene.characters
            )
        ]

    def outline(self) -> list[str]:
        return [scene.one_line() for scene in self.scenes]
