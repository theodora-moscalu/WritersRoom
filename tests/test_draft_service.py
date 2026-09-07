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
    # Re-parsed after an edit
    #

    time.sleep(0.01)
    path.write_text(SCENE_ONE + SCENE_TWO, encoding="utf-8")

    updated = service.current(str(path))
    assert updated is not draft
    assert len(updated.scenes) == 2

    print()
    print("DraftService tests passed.")


if __name__ == "__main__":
    main()
