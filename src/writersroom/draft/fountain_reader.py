import re
from pathlib import Path

from writersroom.draft.base_reader import DraftReader
from writersroom.draft.draft import Draft, DraftScene


class FountainReader(DraftReader):
    """A structural parser for Fountain screenplay files."""

    extensions = (".fountain", ".spmd", ".txt")

    _heading = re.compile(
        r"^(INT|EXT|EST|INT\.?/EXT|I/E)[\. ]",
        re.IGNORECASE,
    )
    _boneyard = re.compile(r"/\*.*?\*/", re.DOTALL)
    _note = re.compile(r"\[\[.*?\]\]", re.DOTALL)
    _cue_extension = re.compile(r"\s*\([^)]*\)\s*$")

    def read(self, path: str) -> Draft:
        raw = Path(path).read_text(encoding="utf-8", errors="replace")

        text = self._note.sub("", self._boneyard.sub("", raw))
        lines = text.splitlines()

        scenes: list[DraftScene] = []
        current: DraftScene | None = None
        body: list[str] = []
        number = 0
        previous_blank = True

        def flush():
            if current is not None:
                current.text = "\n".join(body).strip()

        for line in lines:
            stripped = line.strip()

            heading = self._scene_heading(stripped)

            if heading is not None:
                flush()
                number += 1
                current = DraftScene(number=number, heading=heading, text="")
                scenes.append(current)
                body = []
                previous_blank = True
                continue

            if current is None:
                previous_blank = not stripped
                continue

            if stripped.startswith("=") and not stripped.startswith("=="):
                current.synopsis = stripped.lstrip("= ").strip()
                continue

            if stripped.startswith("#"):
                continue

            cue = self._character_cue(stripped, previous_blank)
            if cue:
                if cue not in current.characters:
                    current.characters.append(cue)

            body.append(line)
            previous_blank = not stripped

        flush()

        return Draft(
            scenes=scenes,
            source_path=path,
            format="fountain",
        )

    def _scene_heading(self, stripped: str) -> str | None:
        if self._heading.match(stripped):
            return stripped

        if (
            stripped.startswith(".")
            and not stripped.startswith("..")
            and len(stripped) > 1
        ):
            return stripped[1:].strip()

        return None

    def _character_cue(self, stripped: str, previous_blank: bool) -> str:
        if stripped.startswith("@"):
            name = stripped[1:]
        elif (
            previous_blank
            and stripped
            and stripped == stripped.upper()
            and any(c.isalpha() for c in stripped)
            and not stripped.endswith(("TO:", ":"))
            and not stripped.startswith(">")
        ):
            name = stripped
        else:
            return ""

        name = self._cue_extension.sub("", name)
        name = name.rstrip("^").strip()

        return name.title() if name.isupper() else name
