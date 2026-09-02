from pathlib import Path
import tempfile

import streamlit as st

from writersroom.application import (
    Application,
)
from writersroom.domains.enums.knowledge_source_type import (
    KnowledgeSourceType,
)
from writersroom.review.review_decision import (
    ReviewDecision,
)


@st.cache_resource
def get_application():
    """Create the WritersRoom application."""

    return Application()


application = get_application()

st.set_page_config(
    page_title="WritersRoom",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 WritersRoom")

st.write(
    """
    Welcome to WritersRoom.

    This application helps build a permanent storytelling
    knowledge library from books, screenplays and other
    storytelling sources.
    """
)

st.divider()

st.subheader("Knowledge")

uploaded_file = st.file_uploader(
    "Choose a document",
    type=[
        "pdf",
        "txt",
        "docx",
    ],
)

knowledge_source_name = ""

if uploaded_file is not None:

    knowledge_source_name = Path(
        uploaded_file.name
    ).stem

knowledge_source_name = st.text_input(
    "Knowledge Source",
    value=knowledge_source_name,
)

knowledge_source_type = st.selectbox(
    "Knowledge Source Type",
    options=list(KnowledgeSourceType),
    format_func=lambda item: item.value,
)

if st.button("📚 Import Document"):

    if uploaded_file is None:

        st.warning(
            "Please choose a document first."
        )

    elif not knowledge_source_name.strip():

        st.warning(
            "Please enter a knowledge source name."
        )

    else:

        suffix = Path(
            uploaded_file.name
        ).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_path = temp_file.name

        result = (
            application.import_service.import_document(
                knowledge_source_name=knowledge_source_name,
                knowledge_source_type=knowledge_source_type,
                path=temp_path,
                document_name=Path(
                    uploaded_file.name
                ).stem,
            )
        )

        if result.success:

            st.session_state.import_result = (
                result.data
            )

            st.session_state.knowledge_source_name = (
                knowledge_source_name
            )

            st.success(
                result.message
            )

        else:

            st.error(result.message)

if st.button("🧠 Extract Knowledge"):

    if (
        "import_result"
        not in st.session_state
    ):

        st.warning(
            "Please import a document first."
        )

    else:

        import_result = (
            st.session_state.import_result
        )

        with st.spinner(
            "Extracting storytelling knowledge..."
        ):

            extraction_result = (
                application.knowledge_pipeline_service.process(
                    knowledge_source_name=(
                        st.session_state.knowledge_source_name
                    ),
                    document_name=(
                        import_result.document.name
                    ),
                    processed_document=(
                        import_result.processed_document
                    ),
                )
            )

        st.session_state.extraction_result = (
            extraction_result
        )

        st.success(
            "Knowledge extraction complete."
        )

        st.write(
            f"Extracted "
            f"{len(extraction_result.items)} "
            f"knowledge item(s)."
        )

if st.button("✅ Review Claims"):

    if (
        "extraction_result"
        not in st.session_state
    ):

        st.warning(
            "Please extract knowledge first."
        )

    else:

        st.session_state.review_mode = True

if (
    st.session_state.get(
        "review_mode",
        False,
    )
):

    st.divider()

    st.subheader(
        "Review Extracted Knowledge"
    )

    extraction_result = (
        st.session_state.extraction_result
    )

    if not extraction_result.items:

        st.info(
            "There are no knowledge items to review."
        )

    else:

        for index, item in enumerate(
            extraction_result.items
        ):

            st.markdown(
                f"### Knowledge Item {index + 1}"
            )

            st.write(
                f"**Level:** "
                f"{item.claim.knowledge_level}"
            )

            st.write(
                f"**Domain:** "
                f"{item.claim.knowledge_domain}"
            )

            st.write(
                f"**Claim:** "
                f"{item.claim.text}"
            )

            st.write(
                f"**Explanation:** "
                f"{item.claim.explanation}"
            )

            current_decision = (
                item.decision
            )

            decision = st.radio(
                "Decision",
                options=[
                    ReviewDecision.ACCEPT,
                    ReviewDecision.REJECT,
                ],
                format_func=lambda value: (
                    "Approve"
                    if value
                    == ReviewDecision.ACCEPT
                    else "Reject"
                ),
                index=(
                    0
                    if current_decision
                    == ReviewDecision.ACCEPT
                    else 1
                ),
                key=f"review_decision_{index}",
                horizontal=True,
            )

            item.decision = decision

            st.divider()

        if st.button(
            "💾 Save Review"
        ):

            knowledge_source_name = (
                st.session_state.knowledge_source_name
            )

            document_name = (
                st.session_state.import_result
                .document.name
            )

            approved = 0
            rejected = 0

            for item in (
                extraction_result.items
            ):

                if (
                    item.decision
                    == ReviewDecision.ACCEPT
                ):

                    result = (
                        application.claim_service.add_extracted_claim(
                            knowledge_source_name=(
                                knowledge_source_name
                            ),
                            document_name=(
                                document_name
                            ),
                            extracted=item.claim,
                        )
                    )

                    if not result.success:

                        st.error(
                            result.message
                        )

                    else:

                        approved += 1

                elif (
                    item.decision
                    == ReviewDecision.REJECT
                ):

                    rejected += 1

            st.session_state.review_mode = (
                False
            )

            st.success(
                f"Review saved. "
                f"Approved: {approved}. "
                f"Rejected: {rejected}."
            )

st.button("🔍 Search Library")

st.divider()

st.caption(
    f"Current project: {application.project.title}"
)

st.caption(
    "WritersRoom Developer Preview"
)