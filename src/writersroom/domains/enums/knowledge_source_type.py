from enum import Enum


class KnowledgeSourceType(Enum):
    """The type of knowledge source."""

    BOOK = "Book"
    SCREENPLAY = "Screenplay"
    ARTICLE = "Article"
    INTERVIEW = "Interview"
    PODCAST = "Podcast"
    COURSE = "Course"
    TRANSCRIPT = "Transcript"
    VIDEO = "Video"
    WEB_PAGE = "Web Page"
    RESEARCH_PAPER = "Research Paper"
    WRITING_NOTE = "Writing Note"