from dataclasses import dataclass


@dataclass
class ExtractedProvenance:
    """Evidence supporting an extracted claim."""

    passage_sequence: int

    confidence: float = 1.0