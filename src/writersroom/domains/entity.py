from abc import ABC, abstractmethod


class Entity(ABC):
    """Base class for all domain entities."""

    @property
    @abstractmethod
    def identity(self) -> str:
        """Return the entity's stable identity."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Return the entity's human-readable name."""
        pass