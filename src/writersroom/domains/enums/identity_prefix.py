from enum import Enum


class IdentityPrefix(Enum):
    """Prefixes used when generating identities."""

    PROJECT = "PR"
    CHARACTER = "CH"
    RELATIONSHIP = "RL"
    LOCATION = "LO"
    EPISODE = "EP"
    SCENE = "SC"
    NOTE = "NT"

    KNOWLEDGE_SOURCE = "KS"
    DOCUMENT = "DOC"
    PASSAGE = "PAS"
    CLAIM = "CL"
    PROVENANCE = "PV"

    WRITER_PROFILE = "WP"