from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)


def main():
    print("Testing KnowledgeSourceType...")

    assert (
        KnowledgeSourceType.BOOK.value
        == "Book"
    )

    assert (
        KnowledgeSourceType.SCREENPLAY.value
        == "Screenplay"
    )

    assert (
        KnowledgeSourceType.COURSE.value
        == "Course"
    )

    assert (
        KnowledgeSourceType.TRANSCRIPT.value
        == "Transcript"
    )

    assert (
        KnowledgeSourceType.RESEARCH_PAPER.value
        == "Research Paper"
    )

    expected = {
        "Book",
        "Screenplay",
        "Article",
        "Interview",
        "Podcast",
        "Course",
        "Transcript",
        "Video",
        "Web Page",
        "Research Paper",
        "Writing Note",
    }

    assert {
        source_type.value
        for source_type in KnowledgeSourceType
    } == expected

    print("KnowledgeSourceType tests passed.")


if __name__ == "__main__":
    main()