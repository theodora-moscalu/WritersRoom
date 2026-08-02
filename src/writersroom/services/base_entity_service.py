from abc import ABC, abstractmethod

from writersroom.common.result import Result


class BaseEntityService(ABC):
    """Base class for services managing collections of domain entities."""

    def __init__(self, project):
        self.project = project

    def add(self, name: str) -> Result:
        """Add a new entity."""

        name = name.strip()

        if not name:
            return Result.fail(f"{self.entity_name} name cannot be empty.")

        if self.find(name):
            return Result.fail(
                f"{self.entity_name} '{name}' already exists."
            )

        entity = self.create_entity(name)

        self.add_to_project(entity)

        self.project.save()

        return Result.ok(
            f"Added {self.entity_name.lower()} '{name}'.",
            data=entity,
        )

    def list(self) -> Result:
        """Return all entities."""

        return Result.ok(
            data=self.get_collection(),
        )

    @property
    @abstractmethod
    def entity_name(self) -> str:
        """Human-readable name of the entity."""
        pass

    @abstractmethod
    def create_entity(self, name: str):
        """Create a new entity."""
        pass

    @abstractmethod
    def find(self, name: str):
        """Find an entity by name."""
        pass

    @abstractmethod
    def add_to_project(self, entity):
        """Add an entity to the project."""
        pass

    @abstractmethod
    def get_collection(self):
        """Return the project's collection of entities."""
        pass