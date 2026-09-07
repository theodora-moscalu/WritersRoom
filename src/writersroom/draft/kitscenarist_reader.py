import re
import sqlite3
import xml.etree.ElementTree as ET

from writersroom.draft.base_reader import DraftReader
from writersroom.draft.draft import Draft, DraftScene


class KitScenaristReader(DraftReader):
    """Reads the current script out of a KIT Scenarist .kitsp project file."""

    extensions = (".kitsp",)

    _heading_like = re.compile(r"^(INT|EXT|EST|I/E|N?T\.)", re.IGNORECASE)
    _cue_extension = re.compile(r"\s*\([^)]*\)\s*$")

    def read(self, path: str) -> Draft:
        xml = self._scenario_xml(path)
        root = ET.fromstring(xml)

        scenes: list[DraftScene] = []
        current: DraftScene | None = None
        blocks: list[str] = []
        number = 0

        leading_heading = self._leading_heading(root)

        def flush():
            if current is not None:
                current.text = "\n".join(blocks).strip()

        for child in root:

            value = self._value(child)

            if child.tag == "scene_heading":
                flush()
                number += 1
                current = DraftScene(number=number, heading=value or "SCENE")
                scenes.append(current)
                blocks = []
                continue

            if current is None:
                flush()
                number += 1
                current = DraftScene(
                    number=number,
                    heading=leading_heading or "OPENING",
                )
                scenes.append(current)
                blocks = []
                if leading_heading and child.tag == "note":
                    # the leading note was promoted to the heading
                    continue

            if not value:
                continue

            if child.tag == "note":
                continue

            if child.tag == "character":
                name = self._character_name(value)
                if name and name.lower() not in {
                    c.lower() for c in current.characters
                }:
                    current.characters.append(name)
                blocks.append("")
                blocks.append(value.strip().upper())
            elif child.tag == "parenthetical":
                blocks.append(value.strip())
            elif child.tag == "dialog":
                blocks.append(value.strip())
            elif child.tag == "transition":
                blocks.append("")
                blocks.append(value.strip().upper())
            else:  # action, shot, lyrics, anything else
                blocks.append("")
                blocks.append(value.strip())

        flush()

        return Draft(
            scenes=[scene for scene in scenes if scene.text or scene.heading],
            source_path=path,
            format="kitscenarist",
        )

    #
    # Helpers
    #

    def _scenario_xml(self, path: str) -> str:
        connection = sqlite3.connect(
            f"file:{path}?mode=ro",
            uri=True,
        )
        connection.row_factory = sqlite3.Row

        try:
            row = connection.execute(
                "SELECT text FROM scenario WHERE is_draft = 0 ORDER BY id LIMIT 1"
            ).fetchone()

            if row is None:
                row = connection.execute(
                    "SELECT text FROM scenario ORDER BY id LIMIT 1"
                ).fetchone()
        finally:
            connection.close()

        if row is None:
            return "<scenario version='1.0'></scenario>"

        return row["text"]

    def _value(self, element) -> str:
        node = element.find("v")

        return (node.text or "") if node is not None else ""

    def _leading_heading(self, root) -> str:
        for child in root:
            if child.tag == "scene_heading":
                return ""

            if child.tag == "note":
                value = self._value(child).strip()
                if self._heading_like.match(value):
                    return value
                return ""

            if child.tag in ("action", "character", "dialog"):
                return ""

        return ""

    def _character_name(self, raw: str) -> str:
        name = self._cue_extension.sub("", raw.strip()).rstrip("^").strip()

        return name.title() if name.isupper() else name
