# WritersRoom — Working Guide for Claude

## What this project is

WritersRoom is **not an AI that writes television**. It is a reasoning system that helps
humans create television by combining structured knowledge, evidence-based reasoning, and
specialised creative collaboration. Text generation is one capability, not the goal — good
writing follows good decisions (ADR-009).

The long-term moat is the **accumulated screenwriting knowledge graph** (thousands of books,
scripts, and interviews reduced to millions of interlinked claims with provenance), not the
language model. Models are interchangeable; the knowledge base is not.

## The four layers

```
Knowledge  →  Retrieval  →  Reasoning  →  Generation
(what is known)  (find it)   (weigh it)   (express it)
```

These are separate architectural layers (ADR-007). **Language models participate only in
reasoning and generation — never as the canonical store of knowledge.**

## Architectural principles

The canonical, authoritative source is
[src/writersroom/domains/docs/architecture_decision_records.md](src/writersroom/domains/docs/architecture_decision_records.md).
Read it before designing any feature. Every feature is evaluated against these ADRs first; a
feature that conflicts with an ADR means redesigning the feature or consciously updating the
ADR after discussion. Summary:

| ADR | Principle |
|-----|-----------|
| 001 | **Stable identity.** Every domain *entity* exposes `identity` and `display_name` (see `domains/entity.py`). The rest of the system depends on that abstraction, not on how identity is represented. |
| 002 | **Single source of truth.** Every fact is stored exactly once; everything else is derived (e.g. an Episode derives its characters from its Scenes). |
| 003 | **Single ownership.** Every entity has exactly one owner; all other links are references. Project owns Characters/Locations; Scenes reference them. |
| 004 | **Knowledge is independent of projects.** Knowledge belongs to the Workspace. Projects consume knowledge; they never own it. Import a screenplay once, benefit every project. |
| 005 | **Claims are the atomic unit of knowledge.** Documents are *sources*; claims are *knowledge*. Reasoning happens over structured claims, not raw documents. |
| 006 | **Knowledge is append-only.** Claims are never silently replaced. Conflicting claims coexist (McKee vs Snyder vs Mazin); status moves Active → Superseded / Disputed / Deprecated. Reasoning resolves disagreement. |
| 007 | **Separate Knowledge / Retrieval / Reasoning / Generation.** The model is not the system's memory. |
| 008 | **Explainability.** Every recommendation carries an inspectable reasoning trace: evidence, supporting claims, assumptions, trade-offs, confidence. Agents produce *(recommendation, reasoning trace)*, not just an answer. |
| 009 | **Optimise decisions, not text.** Before generating Scene 12, the system asks whether it fits the arc, advances the A story, pays off earlier promises, introduces contradictions, preserves theme, holds pacing, supports the season arc. |
| 010 | **Domain first.** The domain model must not depend on AI infrastructure. `Character` never imports an LLM; `Episode` never knows about embeddings; `Scene` never contains prompts; `Knowledge` never knows which model extracted it. Infrastructure depends on the domain, not the reverse. |
| 011 | **Specialist agents.** Build a writers' room, not one super-agent (Showrunner, Story Editor, Dialogue Coach, Character Psychologist, Continuity Editor, Researcher, Theme Analyst, Producer…). Each specialises, each contributes evidence; the Showrunner synthesises the final recommendation. |
| 012 | **Entities vs Value Objects.** Not every domain class is an Entity. Entities exist in the story world or project model (Scene, Character, Episode); value objects are relationships, notes, enums, results, provenance. `Project` is arguably not an entity; a `Note` is metadata on one. Inherit `Entity` only with a genuine stable identity. |
| 013 | **Ownership vs peers.** Children are owned by their parent; relationships between peers use identities, never object references. |
| 014 | **A claim knows where to find its evidence, not why it is true.** It holds provenance (source document + passage, confidence, reviewed) — not an embedded justification. |
| 015 | **Knowledge tiers.** Project knowledge (one workspace) / general storytelling knowledge (shared across workspaces) / external world knowledge (one workspace). |
| 016 | **Ingestion processes `SourceUnit`s, not passages.** |
| 017 | **Never trust LLM output — validate everything.** Extraction output is parsed and every field checked; malformed records are dropped, never guessed or repaired silently. |
| 018 | **The Knowledge Library owns retrieval,** delegated to interchangeable strategies (embeddings first, graph retrieval later) behind an abstraction. |
| 019 | **`ClaimRepository` is the only thing that knows how claims are stored.** It gives read access to accepted knowledge; nobody else touches persistence. |
| 020 | **The knowledge library is stored in SQLite behind `KnowledgeRepository`;** embeddings are derived data persisted in the same DB and rebuilt on demand. |
| 021 | **The Showrunner is retrieval-augmented** — each turn it grounds its answer in retrieved claims + project state and cites its evidence. |
| 022 | **Workspaces are series; knowledge is tiered.** Writing knowledge is shared across workspaces; general and project knowledge belong to one workspace. One SQLite DB, scoped by `tier` + `project_id`. |
| 023 | **The series bible is imported, not typed.** PowerPoint/doc → `StoryBibleExtractor` (Sonnet, structured JSON) → extract → review → merge into enriched `Character` / `Episode` / `Season` by name, additively. |

## Structural model

```
Workspace
├── Knowledge      what do we know?      (shared across projects)
├── Projects       what are we creating? (The Wine Game, Constantinople, …)
└── Agents         how do we think?
```

Knowledge tiers:

- **Project knowledge** (one workspace): Story Bible, Characters, Relationships graph,
  Episodes, Scenes, Project Notes.
- **General storytelling knowledge** (shared across workspaces): screenwriting books,
  screenplays, writing notes, interviews, personal writing style, research.
- **External / world knowledge** (one workspace): wine, history, geography, other research.

WritersRoom as a product = **Knowledge Library** (import / extract / review / retrieve) +
**Writing Engine** (Showrunner / Scene Writer / Dialogue / Rewriting) + **Development Tools**
(Story Bible / Characters / Outline / Timeline). The Knowledge Library is infrastructure, not
the end-user product.

## Codebase conventions

- **Layout.** Composition root in [src/writersroom/application.py](src/writersroom/application.py)
  wires everything. `domains/` = pure domain model (no infra imports). `services/` = use-case
  coordination. `agents/` = LLM-backed specialists. `database/`, `retrieval/`, `importers/`,
  `processors/`, `extraction/`, `review/`, `llm/` = infrastructure. `commands/` + `ui/` = entry
  surfaces (CLI and Streamlit).
- **Dependency injection.** Constructors take optional collaborators defaulting to a concrete
  implementation — e.g. `Agent(name, prompt_file, llm=None)` falls back to `OllamaClient()`;
  `ExtractionService(librarian=None, transformer=None)`. Swap behaviour by injecting, not by
  editing the class.
- **Pluggable strategy = factory.** Provider/strategy selection lives in a small factory
  (`llm/llm_factory.py`, `ProcessorFactory`, `ImporterFactory`, `RetrievalContainer`), driven
  by config or classification — not `if` chains scattered through call sites.
- **Identity.** `KnowledgeRepository.next_identity(prefix)` / `ProjectRepository` allocate ids
  from typed prefixes in `domains/enums/identity_prefix.py` (`CL` claim, `KS` source, `PR`
  project…), counters stored in the DB. Project *sub*-entities (Character, Scene…) still use
  their `name` as identity within the blob.
- **Persistence (ADR-020, ADR-022).** One SQLite database (`workspace/knowledge.db`) holds
  everything, reached only through the `database/` repositories — no ORM, hand-written SQL.
  `KnowledgeRepository` owns the library; `ProjectRepository` stores each project (= workspace
  = series) as one JSON blob row in the `projects` table. `EmbeddingRepository` holds derived
  vectors. `database/legacy_import.py` migrates `projects/*.json` and any old `workspace.json`
  library on first run; `Workspace` and `workspace_import.py` are gone.
- **Knowledge tiers (ADR-022).** `knowledge_sources.tier` is `writing` (craft — shared by every
  workspace, `project_id` NULL) or `general` (world/research — one workspace). Services and
  `RetrievalContainer` take a `project_id`; `KnowledgeRepository.list_claims(project_id)` and
  `_scope_clause()` return writing ∪ that workspace's general. `Application` rebinds all
  scoped services + rebuilds the index on a workspace switch (`open_project` / `create_project`).
  World-tier *extraction* isn't built yet — a `general` import stores passages only.
- **House style.** Very vertical: one argument per line, blank line between statements, imports
  wrapped in parens. Match the surrounding file.
- **LLM infrastructure.** `.env` is loaded once in `src/writersroom/__init__.py` via
  `python-dotenv`. Knowledge extraction (`WRITERSROOM_EXTRACTION_PROVIDER`) and the Showrunner
  (`WRITERSROOM_SHOWRUNNER_PROVIDER`) both default to Claude Sonnet (`claude-sonnet-5`) through
  `llm/anthropic_client.py`, built by `llm/llm_factory.py`; set either to `ollama` to switch
  back. Embeddings and `RelationshipAnalyser` still use Ollama. Extraction output is a
  **plain-text block format** (`LEVEL:` / `DOMAIN:` / …), normalized then parsed — not JSON.
- **Retrieval-augmented Showrunner (ADR-021).** Each turn, `Showrunner.respond()` builds a
  transient system prompt = base prompt + `ProjectContextBuilder` (the project's characters /
  relationships / seasons / episodes / notes, with the enriched fields) + `KnowledgeContextBuilder`
  (top claims from the library for that message, via `RetrievalContainer.search_service`). It's
  told to ground suggestions in those claims, cite their ids, and end with `Grounded in: [CL…]`.
  `Application` calls `RetrievalContainer.build_index()` at startup (guarded — Ollama may be down).
- **Bible import (ADR-023).** `bible import <path>` (CLI) / the Story Bible panel (Streamlit) →
  `PptxImporter` (or docx/pdf) → `StoryBibleExtractor` (`agents/`, Sonnet, `respond_json`) →
  `BiblePipelineService.extract` builds a `BibleReview` matched against the project →
  writer keeps/skips → `.apply` merges by name. `Character` / `Episode` gained fields;
  `domains/story/season.py` is new; `Season` references episodes by title.

## Tests

- `tests/test_*.py` are **standalone scripts** with a `def main()` and `assert`s, run directly
  (`uv run python tests/test_extraction_service.py`). No pytest, no mocking — they exercise the
  real pipeline, so LLM-touching tests need `ANTHROPIC_API_KEY` (or the Ollama fallback) and a
  running Ollama for embeddings.
- `tests/support.py` — `knowledge_repository()` returns a `KnowledgeRepository` over an
  in-memory SQLite DB; `limit_source_units()` caps the end-to-end PDF tests to the first 3
  scenes (one LLM call each) — `WRITERSROOM_E2E_SCENE_LIMIT=0` runs the whole document.
- Routine runs: `WRITERSROOM_EXTRACTION_PROVIDER=ollama WRITERSROOM_SHOWRUNNER_PROVIDER=ollama`
  keeps the LLM-touching tests off the paid API.

## Commands

```bash
uv sync                                        # install / update deps
uv run python -m writersroom.main              # CLI
uv run streamlit run src/writersroom/ui/app.py # Streamlit UI
uv run python tests/test_<name>.py             # run one test script
uv add <pkg>                                   # add a dependency (updates pyproject + uv.lock)
```

## Pointers

- Architecture diagram: [info/architecture.md](info/architecture.md)
- ADRs (canonical): [src/writersroom/domains/docs/architecture_decision_records.md](src/writersroom/domains/docs/architecture_decision_records.md)
