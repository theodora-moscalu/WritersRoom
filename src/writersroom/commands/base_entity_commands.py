from abc import ABC, abstractmethod


class BaseEntityCommands(ABC):
    """Base class for entity command handlers."""

    def __init__(self, command_name: str, service):
        self.command_name = command_name
        self.service = service

    @property
    @abstractmethod
    def entity_name(self) -> str:
        """Singular entity name."""

    @property
    @abstractmethod
    def entity_name_plural(self) -> str:
        """Plural entity name."""

    def handle(self, args: list[str]) -> bool:
        """Handle an entity command."""

        if not args:
            self.print_help()
            return True

        action = args[0].lower()

        if action == "add":
            self.add(args[1:])
            return True

        if action == "list":
            self.list()
            return True

        return self.handle_custom_command(action, args[1:])

    def handle_custom_command(
        self,
        action: str,
        args: list[str],
    ) -> bool:
        """Handle entity-specific commands.

        Subclasses can override this to support additional commands.
        """

        print(
            f"\nUnknown {self.entity_name.lower()} command '{action}'.\n"
        )

        return True

    def add(self, args: list[str]):
        """Add a new entity."""

        if not args:
            print(
                f"\nPlease provide a {self.entity_name.lower()} name.\n"
            )
            return

        result = self.service.add(" ".join(args))

        print(f"\n{result.message}\n")

    def list(self):
        """List all entities."""

        result = self.service.list()

        print()

        print(self.entity_name_plural)
        print("-" * len(self.entity_name_plural))

        if result.data:
            for entity in result.data:
                print(entity)
        else:
            print(f"No {self.entity_name_plural.lower()} found.")

        print()

    def print_help(self):
        """Display available commands."""

        print()
        print(f"{self.entity_name} commands")
        print("-" * (len(self.entity_name) + 9))
        print(f"{self.command_name} add <name>")
        print(f"{self.command_name} list")
        self.print_custom_help()
        print()

    def print_custom_help(self):
        """Display entity-specific help.

        Subclasses can override this.
        """

        pass