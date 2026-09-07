import tempfile
import time
from pathlib import Path

from writersroom.services.draft_service import DraftService


SCENE_ONE = """INT. BAR - NIGHT

Zoe drinks alone.
"""

SCENE_TWO = """
EXT. STREET - NIGHT

Zoe leaves.
"""


def main():
    print("Testing DraftService...")

    service = DraftService()

    assert service.current(None) is None
    assert service.current("nope.fountain") is None

    path = Path(tempfile.mkdtemp()) / "draft.fountain"
    path.write_text(SCENE_ONE, encoding="utf-8")

    draft = service.current(str(path))
    assert draft is not None
    assert len(draft.scenes) == 1

    #
    # Cached while unchanged
    #

    assert service.current(str(path)) is draft

    #
    # Re-parsed after an edit, and the changed scene is flagged
    #

    time.sleep(0.01)
    path.write_text(SCENE_ONE + SCENE_TWO, encoding="utf-8")

    updated = service.current(str(path))
    assert updated is not draft
    assert len(updated.scenes) == 2
    assert updated.changed_scenes == [2]  # scene 2 is new
    assert updated.latest_change().number == 2

    #
    # Edit an existing scene's body -> that scene number is flagged
    #

    time.sleep(0.01)
    path.write_text(
        SCENE_ONE.replace("drinks alone", "downs a whisky") + SCENE_TWO,
        encoding="utf-8",
    )

    edited = service.current(str(path))
    assert edited.changed_scenes == [1]

    print()
    print("DraftService tests passed.")


if __name__ == "__main__":
    main()
