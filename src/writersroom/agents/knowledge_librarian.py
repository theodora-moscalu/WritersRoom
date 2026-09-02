from writersroom.agents.base_agent import (
    Agent,
)
from writersroom.extraction.extraction_batch import (
    ExtractionBatch,
)
from writersroom.extraction.extraction_unit import (
    ExtractionUnit,
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
        unit: ExtractionUnit,
    ) -> list[KnowledgeRecord]:
        """Analyse a single extraction unit."""

        return self.analyse_batch(
            ExtractionBatch(
                [unit]
            )
        )

    def analyse_batch(
        self,
        batch: ExtractionBatch,
    ) -> list[KnowledgeRecord]:
        """Analyse a batch of extraction units."""

        text = []

        for index, unit in enumerate(
            batch,
            start=1,
        ):

            text.append(
                f"===== SOURCE {index} ====="
            )

            if unit.heading:

                text.append(
                    unit.heading
                )

            text.append("")

            text.append(
                unit.text
            )

            text.append("")

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": "\n".join(text),
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