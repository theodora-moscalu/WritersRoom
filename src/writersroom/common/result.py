from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Result:
    """Represents the outcome of an operation."""

    success: bool
    message: str = ""
    data: Any = None

    @classmethod
    def ok(cls, message: str = "", data: Any = None):
        """Create a successful result."""

        return cls(
            success=True,
            message=message,
            data=data,
        )

    @classmethod
    def fail(cls, message: str):
        """Create a failed result."""

        return cls(
            success=False,
            message=message,
        )