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

#
# Workspace selector — a workspace is one TV series.
#

projects = application.list_projects()
project_titles = {identity: title for identity, title in projects}
NEW_WORKSPACE = "➕ New workspace…"

with st.sidebar:

    st.subheader("Workspace")

    options = list(project_titles) + [NEW_WORKSPACE]

    default_index = (
        options.index(application.project.identity)
        if application.project.identity in project_titles
        else 0
    )

    choice = st.selectbox(
        "Current workspace",
        options=options,
        index=default_index,
        format_func=lambda value: (
            NEW_WORKSPACE
            if value == NEW_WORKSPACE
            else project_titles[value]
        ),
    )

    if choice == NEW_WORKSPACE:

        new_title = st.text_input("New workspace name")

        if st.button("Create workspace") and new_title.strip():
            application.create_project(new_title.strip())
            st.rerun()

    elif choice != application.project.identity:
        application.open_project(choice)
        st.rerun()

st.caption(
    f"Workspace: {application.project.title}"
)

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

knowledge_tier = st.radio(
    "Knowledge Tier",
    options=["writing", "general"],
    format_func=lambda value: (
        "Writing — screenwriting craft, shared by every workspace"
        if value == "writing"
        else "General — world / research, this workspace only"
    ),
    horizontal=False,
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
                tier=knowledge_tier,
            )
        )

        if result.success:

            st.session_state.import_result = (
                result.data
            )

            st.session_state.knowledge_source_name = (
                knowledge_source_name
            )

            st.session_state.knowledge_tier = knowledge_tier

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

    elif (
        st.session_state.get("knowledge_tier") == "general"
    ):

        st.info(
            "World-knowledge extraction is not enabled yet. "
            "The passages are stored; only Writing-tier sources are extracted."
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

#
# Story Bible — import structured project data from a document
#

st.subheader("📖 Story Bible")

st.caption(
    f"Import a bible for **{application.project.title}** "
    "(characters, seasons, episodes, notes)."
)

bible_file = st.file_uploader(
    "Choose a bible document",
    type=["pptx", "docx", "pdf"],
    key="bible_upload",
)

if st.button("🧾 Extract Bible"):

    if bible_file is None:
        st.warning("Please choose a document first.")
    else:
        suffix = Path(bible_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(bible_file.getbuffer())
            temp_path = temp_file.name

        with st.spinner("Reading the bible..."):
            st.session_state.bible_review = (
                application.bible_pipeline.extract(
                    temp_path,
                    application.project,
                )
            )

if "bible_review" in st.session_state:

    review = st.session_state.bible_review

    for warning in review.warnings:
        st.warning(warning)

    if not review.items:
        st.info("Nothing to import from this document.")
    else:
        st.write(f"**{len(review.items)} proposed entities**")

        keep = {}

        for index, item in enumerate(review.items):
            keep[index] = st.checkbox(
                item.label(),
                value=True,
                key=f"bible_keep_{index}",
            )

        if st.button("✅ Apply to Workspace"):

            from writersroom.review.review_decision import (
                ReviewDecision as _RD,
            )

            for index, item in enumerate(review.items):
                if not keep[index]:
                    item.decision = _RD.REJECT

            result = application.bible_pipeline.apply(
                application.project,
                review,
            )
            application.save_project()

            del st.session_state.bible_review
            st.success(result.message)
            st.rerun()

st.divider()

#
# Script
#

st.subheader("🎬 Script")

_draft_path = st.text_input(
    "Script file (KIT Scenarist .kitsp or Fountain)",
    value=application.project.draft_path,
    placeholder="C:/path/to/The Wine Game.kitsp",
)

_cols = st.columns(2)

if _cols[0].button("Link script") and _draft_path.strip():
    application.project.draft_path = _draft_path.strip()
    application.save_project()
    st.rerun()

if _cols[1].button("Unlink") and application.project.draft_path:
    application.project.draft_path = ""
    application.save_project()
    st.rerun()

if application.project.draft_path:

    _draft = application.draft_service.current(application.project.draft_path)

    if _draft is None:
        st.warning(
            "Linked, but the file is missing or not a readable script."
        )
    elif not _draft.scenes:
        st.info("No scenes found in the script yet.")
    else:
        st.caption(f"{len(_draft.scenes)} scenes · read {_draft.read_at}")

        _scene = st.selectbox(
            "Scene",
            options=_draft.scenes,
            format_func=lambda s: f"{s.number}. {s.heading}",
        )

        st.text(_scene.text)

st.divider()

#
# Character graph
#

st.subheader("🕸 Character Graph")

from writersroom.graph.character_graph import (
    CharacterGraph as _CharacterGraph,
)

_graph = _CharacterGraph.from_project(application.project)

if not _graph.characters():
    st.caption("No characters yet — import a bible or add characters.")
else:
    st.graphviz_chart(_graph.to_dot())

    _isolated = _graph.isolated()
    if _isolated:
        st.caption("Isolated: " + ", ".join(_isolated))

st.divider()

st.caption(
    f"Current project: {application.project.title}"
)

st.caption(
    "WritersRoom Developer Preview"
)