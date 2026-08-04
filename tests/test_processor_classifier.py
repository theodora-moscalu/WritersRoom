from writersroom.processors.processor_classifier import (
    ProcessorClassifier,
)
from writersroom.processors.processor_type import (
    ProcessorType,
)


def main():
    print(
        "Testing ProcessorClassifier..."
    )

    screenplay = """
INT. HOUSE - DAY

John enters.

MARY
Hello.
"""

    result = (
        ProcessorClassifier.classify(
            screenplay
        )
    )

    assert (
        result
        == ProcessorType.SCENE
    )

    prose = """
Chapter One

Once upon a time there was
a storyteller.
"""

    result = (
        ProcessorClassifier.classify(
            prose
        )
    )

    assert (
        result
        == ProcessorType.PARAGRAPH
    )

    print(
        "ProcessorClassifier tests passed."
    )


if __name__ == "__main__":
    main()