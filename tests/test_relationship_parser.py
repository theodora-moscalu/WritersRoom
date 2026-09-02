from writersroom.relationship.relationship_parser import (
    RelationshipParser,
)


def main():

    print(
        "Testing RelationshipParser..."
    )

    parser = (
        RelationshipParser()
    )

    records = parser.parse(
        ""
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
        "RelationshipParser tests passed."
    )


if __name__ == "__main__":
    main()