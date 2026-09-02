from writersroom.agents.relationship_analyser import (
    RelationshipAnalyser,
)


def main():

    print(
        "Testing RelationshipAnalyser..."
    )

    analyser = (
        RelationshipAnalyser()
    )

    records = (
        analyser.analyse(
            claim_a=None,
            claim_b=None,
        )
    )

    assert isinstance(
        records,
        list,
    )

    assert (
        len(records)
        == 0
    )

    print()

    print(
        "RelationshipAnalyser tests passed."
    )


if __name__ == "__main__":
    main()