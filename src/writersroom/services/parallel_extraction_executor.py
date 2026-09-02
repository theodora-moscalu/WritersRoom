from concurrent.futures import (
    ThreadPoolExecutor,
)


class ParallelExtractionExecutor:
    """Executes extraction tasks in parallel."""

    def __init__(
        self,
        max_workers: int = 4,
    ):
        self.max_workers = (
            max_workers
        )

    def execute(
        self,
        items,
        worker,
    ):
        """Execute work in parallel."""

        with ThreadPoolExecutor(
            max_workers=self.max_workers,
        ) as executor:

            return list(
                executor.map(
                    worker,
                    items,
                )
            )