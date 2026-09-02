import time

from writersroom.services.parallel_extraction_executor import (
    ParallelExtractionExecutor,
)


def square(
    value: int,
) -> int:

    time.sleep(
        0.1
    )

    return value * value


def main():

    print(
        "Testing ParallelExtractionExecutor..."
    )

    executor = (
        ParallelExtractionExecutor(
            max_workers=4,
        )
    )

    results = (
        executor.execute(
            [1, 2, 3, 4],
            square,
        )
    )

    assert (
        results
        == [1, 4, 9, 16]
    )

    print()

    print(
        "ParallelExtractionExecutor tests passed."
    )


if __name__ == "__main__":
    main()