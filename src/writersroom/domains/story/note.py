from datetime import datetime

from writersroom.domains.enums.note_target_type import (
    NoteTargetType,
)


class Note:
    """Represents a note."""

    def __init__(
        self,
        title: str,
        target_type: NoteTargetType,
        target_id: str,
        content: str = "",
        created: str |None = None,
        modified: str |None = None,
    ):
        self.title = title

        self.target_type = target_type
        self.target_id = target_id

        self.content = content

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        self.created = created or now
        self.modified = modified or now

    def update_content(self, content: str):
        """Update the note content."""

        self.content = content

        self.modified = datetime.now().isoformat(
            timespec="seconds"
        )

    def to_dict(self):
        """Convert the note to a dictionary."""

        return {
            "title": self.title,
            "target_type": self.target_type.value,
            "target_id": self.target_id,
            "content": self.content,
            "created": self.created,
            "modified": self.modified,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Note from a dictionary."""

        return cls(
            title=data["title"],
            target_type=NoteTargetType(
                data["target_type"]
            ),
            target_id=data["target_id"],
            content=data.get("content", ""),
            created=data.get("created"),
            modified=data.get("modified"),
        )

    def __str__(self):
        return self.title