from writersroom.domains.enums.identity_prefix import (
    IdentityPrefix,
)


class IdentityGenerator:
    """Generates stable identities backed by the database."""

    def __init__(self, database):
        self.database = database

    def next(self, prefix: IdentityPrefix) -> str:
        """Return the next identity for a prefix."""

        key = prefix.value

        row = self.database.query_one(
            "SELECT value FROM identity_counters WHERE prefix = ?",
            (key,),
        )

        current = (
            row["value"] if row else 0
        ) + 1

        self.database.execute(
            "INSERT INTO identity_counters (prefix, value) "
            "VALUES (?, ?) "
            "ON CONFLICT(prefix) DO UPDATE SET value = excluded.value",
            (key, current),
        )

        return f"{key}{current:06d}"
