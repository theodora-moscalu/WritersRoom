# Architecture Decision Records (ADRs)

This document defines the architectural principles of WritersRoom.

Every new feature should be evaluated against these decisions before implementation.

If a feature conflicts with an ADR, either:

- redesign the feature, or
- consciously update the ADR after discussion.

Architectural decisions are intended to remain stable over the lifetime of the project.

---

# ADR-001 — Stable Identity

## Decision

Every domain entity exposes a stable identity.

Other parts of the system depend on the entity's identity rather than its internal implementation.

## Rationale

Identity should be independent of presentation.

This allows the internal implementation to evolve without changing the rest of the system.

## Consequences

- Every entity exposes an `identity`.
- Every entity exposes a `display_name`.
- Services should use identities rather than directly depending on implementation details.

---

# ADR-002 — Single Source of Truth

## Decision

Every piece of information is stored exactly once.

All other representations are derived.

## Rationale

Duplicated information inevitably becomes inconsistent.

## Examples

Good

Scene
- characters

Episode
- derives its characters from scenes

Bad

Episode
- characters

Scene
- characters

Both storing the same information.

---

# ADR-003 — Single Ownership

## Decision

Every entity has exactly one owner.

All other relationships are references.

## Examples

Project owns Characters.

Scenes reference Characters.

Project owns Locations.

Scenes reference Locations.

## Rationale

Ownership and references must never be confused.

---

# ADR-004 — Knowledge is Independent of Projects

## Decision

Knowledge belongs to the workspace.

Projects consume knowledge.

Projects do not own knowledge.

## Rationale

Knowledge should be reusable across projects.

Importing a screenplay once should benefit every future project.

---

# ADR-005 — Claims are the Atomic Unit of Knowledge

## Decision

Documents are sources.

Claims are knowledge.

## Rationale

Reasoning should happen over structured claims rather than raw documents.

Documents are containers.

Claims are reusable knowledge.

---

# ADR-006 — Knowledge is Append-Only

## Decision

Knowledge is never silently replaced.

Conflicting claims coexist.

Reasoning resolves disagreement.

## Rationale

Creative disciplines rarely have absolute truths.

Different experts often disagree.

The system should preserve competing viewpoints.

---

# ADR-007 — Separate Knowledge, Retrieval, Reasoning and Generation

## Decision

These are separate architectural layers.

Knowledge

↓

Retrieval

↓

Reasoning

↓

Generation

## Rationale

Language models should not become the system's memory.

Knowledge and reasoning should remain independent.

---

# ADR-008 — Explainability

## Decision

Every recommendation must have an inspectable reasoning trace.

## A reasoning trace should eventually include

- evidence
- supporting claims
- assumptions
- trade-offs
- confidence

## Rationale

Users should understand why the system recommends something.

---

# ADR-009 — Optimise Decisions, not Text

## Decision

WritersRoom exists to improve creative decision-making.

Text generation is one capability.

It is not the primary goal.

## Rationale

Good writing follows good decisions.

---

# ADR-010 — Domain First

## Decision

The domain model must remain independent of AI infrastructure.

## Examples

Character never imports an LLM.

Episode never knows about embeddings.

Scene never contains prompts.

Knowledge never depends on Ollama.

## Rationale

Infrastructure changes.

The domain should remain stable.

---

# ADR-011 — Specialist Agents

## Decision

The system consists of specialist agents rather than one monolithic AI.

## Examples

- Showrunner
- Story Editor
- Dialogue Coach
- Character Specialist
- Continuity Editor
- Researcher

## Rationale

Television is written collaboratively.

The architecture should reflect that.

---

# Before Implementing Any Feature

Every feature should be checked against these questions.

## Identity

Does every new entity expose a stable identity?

## Duplication

Am I storing information twice?

## Ownership

Who owns this data?

Who only references it?

## Knowledge

Does this belong in a Project or in the Knowledge Library?

## Claims

Am I storing a document or extracting reusable knowledge?

## Explainability

Can the system explain this recommendation?

## Separation

Am I mixing domain logic with AI infrastructure?

## Collaboration

Should this responsibility belong to a specialist agent instead?

---

These ADRs are intended to evolve slowly.

Changing an ADR is a significant architectural decision.