from writersroom.agents.base_agent import (
    Agent,
)
from writersroom.extraction.knowledge_record import (
    KnowledgeRecord,
)
from writersroom.extraction.normalizers.knowledge_normalizer import (
    KnowledgeNormalizer,
)
from writersroom.extraction.parsers.knowledge_parser import (
    KnowledgeParser,
)
from writersroom.processors.source_unit import (
    SourceUnit,
)


class KnowledgeLibrarian(Agent):
    """AI agent responsible for extracting storytelling knowledge."""

    def __init__(self):
        super().__init__(
            name="Knowledge Librarian",
            prompt_file=(
                "knowledge_librarian.txt"
            ),
        )

        self.normalizer = (
            KnowledgeNormalizer()
        )

        self.parser = (
            KnowledgeParser()
        )

    def analyse(
        self,
        unit: SourceUnit,
    ) -> list[KnowledgeRecord]:
        """Analyse a source unit."""

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": unit.text,
            },
        ]

        response = self.ask_llm(
            messages
        )

        normalized = (
            self.normalizer.normalize(
                response
            )
        )

        return self.parser.parse(
            normalized
        )