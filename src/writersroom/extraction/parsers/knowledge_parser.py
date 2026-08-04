import re

from writersroom.domains.enums.importance import (
    Importance,
)
from writersroom.domains.enums.knowledge_domain import (
    KnowledgeDomain,
)
from writersroom.domains.enums.knowledge_level import (
    KnowledgeLevel,
)
from writersroom.extraction.knowledge_record import (
    KnowledgeRecord,
)


class KnowledgeParser:
    """Parses Knowledge Librarian output."""

    _separator = re.compile(
        r"-{10,}"
    )

    _required_fields = (
        "LEVEL",
        "DOMAIN",
        "IMPORTANCE",
        "TEXT",
        "EXPLANATION",
    )

    def parse(
        self,
        text: str,
    ) -> list[KnowledgeRecord]:
        """Parse knowledge records."""

        records = []

        blocks = [
            block.strip()
            for block in self._separator.split(
                text
            )
            if block.strip()
        ]

        for block in blocks:

            values = self._read_fields(
                block
            )

            if (
                values is None
            ):
                continue

            record = self._build_record(
                values,
                block,
            )

            if (
                record is not None
            ):
                records.append(
                    record
                )

        return records

    def _read_fields(
        self,
        block: str,
    ) -> dict[str, str] | None:
        """Read fields from a knowledge block."""

        values = {}

        current = None

        for line in block.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.endswith(":"):

                current = (
                    line[:-1]
                    .upper()
                )

                values[current] = ""

                continue

            if current:

                if values[current]:

                    values[current] += " "

                values[current] += line

        for field in (
            self._required_fields
        ):

            if (
                field
                not in values
            ):

                print()
                print(
                    "Skipping knowledge record."
                )
                print(
                    f"Missing field: {field}"
                )
                print()

                return None

            if (
                not values[field]
            ):

                print()
                print(
                    "Skipping knowledge record."
                )
                print(
                    f"Empty field: {field}"
                )
                print()

                return None

        return values

    def _build_record(
        self,
        values: dict[
            str,
            str,
        ],
        block: str,
    ) -> KnowledgeRecord | None:
        """Build a KnowledgeRecord."""

        try:

            return KnowledgeRecord(
                knowledge_level=(
                    KnowledgeLevel[
                        values["LEVEL"]
                    ]
                ),
                knowledge_domain=(
                    KnowledgeDomain[
                        values["DOMAIN"]
                    ]
                ),
                importance=(
                    Importance[
                        values[
                            "IMPORTANCE"
                        ]
                    ]
                ),
                text=values["TEXT"],
                explanation=(
                    values[
                        "EXPLANATION"
                    ]
                ),
            )

        except Exception as ex:

            print()
            print(
                "Skipping knowledge record."
            )
            print()
            print(block)
            print()
            print(
                f"{type(ex).__name__}: {ex}"
            )
            print()

            return None