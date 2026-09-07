import tempfile
from pathlib import Path

from writersroom.draft.fountain_reader import FountainReader
from writersroom.draft.reader_factory import DraftReaderFactory


FOUNTAIN = """Title: The Wine Game

INT. AUCTION HOUSE - DAY

= Nadia works the room before the sale.

Nadia scans the lots. Marcus watches her from the doorway.

NADIA
Lot 34 is a fake.

MARCUS (V.O.)
She was always the sharpest in the room. /* note to self: too on the nose? */

.THE CELLAR - LATER

Cold. Concrete. A single bulb.

NADIA (CONT'D)
You forged the provenance.

MARCUS
I taught you everything you know about provenance.

INT. NADIA'S FLAT - NIGHT

Nadia can't sleep.
"""


def main():
    print("Testing FountainReader...")

    path = Path(tempfile.mkdtemp()) / "draft.fountain"
    path.write_text(FOUNTAIN, encoding="utf-8")

    reader = DraftReaderFactory.create(str(path))
    assert isinstance(reader, FountainReader)

    draft = reader.read(str(path))

    assert draft.format == "fountain"
    assert len(draft.scenes) == 3

    s1, s2, s3 = draft.scenes

    assert s1.heading == "INT. AUCTION HOUSE - DAY"
    assert s1.synopsis == "Nadia works the room before the sale."
    assert set(s1.characters) == {"Nadia", "Marcus"}
    assert "note to self" not in s1.text  # boneyard stripped

    assert s2.heading == "THE CELLAR - LATER"  # forced heading, dot stripped
    assert s2.characters == ["Nadia", "Marcus"]

    assert s3.heading == "INT. NADIA'S FLAT - NIGHT"
    assert s3.characters == []

    outline = draft.outline()
    assert outline[0].startswith("1. INT. AUCTION HOUSE - DAY — Nadia works the room")
    assert outline[2].startswith("3. INT. NADIA'S FLAT - NIGHT — Nadia can't sleep")

    print()
    for line in outline:
        print("  " + line)
    print()
    print("FountainReader tests passed.")


if __name__ == "__main__":
    main()
