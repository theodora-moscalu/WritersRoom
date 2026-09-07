import sqlite3
import tempfile
from pathlib import Path

from writersroom.draft.kitscenarist_reader import KitScenaristReader
from writersroom.draft.reader_factory import DraftReaderFactory


SCENARIO_XML = """<?xml version="1.0"?>
<scenario version="1.0">
<note><v><![CDATA[INT. TRADING FLOOR - DAY]]></v></note>
<action><v><![CDATA[Phones ring. ZOE NAKADA works the best desk.]]></v></action>
<character><v><![CDATA[ZOE]]></v></character>
<parenthetical><v><![CDATA[(on phone)]]></v></parenthetical>
<dialog><v><![CDATA[Five percent above market.]]></v></dialog>
<character><v><![CDATA[Zoe ]]></v></character>
<dialog><v><![CDATA[I can do market price.]]></v></dialog>
<scene_heading uuid="{abc}"><v><![CDATA[INT. BOARD ROOM - CONTINUOUS]]></v></scene_heading>
<action><v><![CDATA[HIRO waits. GREG folds his arms.]]></v></action>
<character><v><![CDATA[HIRO]]></v></character>
<dialog><v><![CDATA[Sit down, Zoe.]]></v></dialog>
</scenario>
"""

DRAFT_XML = "<scenario version='1.0'></scenario>"


def build_kitsp(path: Path):
    connection = sqlite3.connect(str(path))
    connection.execute(
        "CREATE TABLE scenario (id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "scheme TEXT NOT NULL, text TEXT NOT NULL, is_draft INTEGER NOT NULL DEFAULT(0))"
    )
    connection.execute(
        "INSERT INTO scenario (scheme, text, is_draft) VALUES ('', ?, 0)",
        (SCENARIO_XML,),
    )
    connection.execute(
        "INSERT INTO scenario (scheme, text, is_draft) VALUES ('', ?, 1)",
        (DRAFT_XML,),
    )
    connection.commit()
    connection.close()


def main():
    print("Testing KitScenaristReader...")

    path = Path(tempfile.mkdtemp()) / "The Wine Game.kitsp"
    build_kitsp(path)

    reader = DraftReaderFactory.create(str(path))
    assert isinstance(reader, KitScenaristReader)

    draft = reader.read(str(path))

    assert draft.format == "kitscenarist"
    assert len(draft.scenes) == 2

    s1, s2 = draft.scenes

    assert s1.heading == "INT. TRADING FLOOR - DAY"  # promoted from the leading note
    assert s1.characters == ["Zoe"]                  # ZOE / "Zoe " deduped
    assert "Five percent above market." in s1.text
    assert "ZOE" in s1.text  # cue rendered

    assert s2.heading == "INT. BOARD ROOM - CONTINUOUS"
    assert s2.characters == ["Hiro"]
    assert "Sit down, Zoe." in s2.text

    #
    # The is_draft=1 row (draft mode scratch) is ignored
    #

    assert draft.scene(1).text != ""

    print()
    for line in draft.outline():
        print("  " + line)
    print()
    print("KitScenaristReader tests passed.")


if __name__ == "__main__":
    main()
