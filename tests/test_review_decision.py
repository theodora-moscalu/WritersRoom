from writersroom.review.review_decision import (
    ReviewDecision,
)


def main():
    print(
        "Testing ReviewDecision..."
    )

    assert (
        ReviewDecision.ACCEPT
        == "accept"
    )

    assert (
        ReviewDecision.REJECT
        == "reject"
    )

    assert (
        ReviewDecision.EDIT
        == "edit"
    )

    print(
        "ReviewDecision tests passed."
    )


if __name__ == "__main__":
    main()