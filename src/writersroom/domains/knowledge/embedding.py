from dataclasses import dataclass
from dataclasses import field


@dataclass
class Embedding:
    """Semantic embedding of a piece of knowledge."""

    model: str

    vector: list[float]

    dimensions: int = field(
        init=False
    )

    def __post_init__(
        self,
    ):
        self.dimensions = len(
            self.vector
        )