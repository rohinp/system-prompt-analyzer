# System Prompt Analyzer — Incremental Delivery Plan

## Product outcome

Help a user understand whether a system prompt gives an agent enough direction to act safely
and predictably. The product should make existing instructions visible, identify loose ends, and
suggest concrete improvements without silently rewriting the user's intent.

The first useful release should answer three questions:

1. What rules, constraints, guards, tools, and workflows are already present?
2. Where could the agent behave ambiguously, exceed its intended scope, or misuse a tool?
3. What targeted instruction could close each gap?

## Delivery principles

- Each increment must leave the application runnable and demonstrable.
- Add one real capability at a time and protect it with tests before moving on.
- Keep analysis results structured; the interface should not have to parse model prose.
- Show evidence from the submitted prompt for every finding.
- Clearly distinguish detected instructions from suggested additions.
- Do not store prompts or API keys unless a later increment explicitly introduces persistence.
- Start with one provider and one prompt-analysis workflow. Generalize only after a second real
  use case requires it.

## Increment 0 — Working scaffold ✅

**Goal:** Establish the smallest end-to-end application.

Already delivered:

- FastAPI application and typed API schemas
- Responsive prompt input and visual result cards
- Deterministic first-pass checks
- Environment-based provider configuration
- Automated API tests and linting

**Completion check:** A user can start the app, submit a prompt, and see detected statements and
potential gaps without configuring an API key.

## Increment 1 — Define the analysis contract ✅

**Goal:** Make “good system prompt” measurable before relying on a model.

Delivered:

- A versioned rubric covering:
  - role and objective
  - scope and non-goals
  - instruction priority and conflict handling
  - tool-use criteria, preconditions, and failure behavior
  - permissions and irreversible actions
  - sensitive-data and safety guards
  - uncertainty and clarification behavior
  - output contract and completion criteria
- Structured finding fields: category, severity, status, evidence, rationale, and recommendation
- Stable identifiers for rubric checks and findings
- A small fixture set containing strong, weak, conflicting, and tool-heavy prompts

Tests delivered:

- Schema validation for every finding type
- Unit tests for deterministic checks
- Snapshot-style tests for representative prompt fixtures

**Completion check:** Every displayed gap maps to a documented rubric rule and includes either
prompt evidence or an explicit explanation that the instruction is missing.

## Increment 2 — Add one model-backed analyzer

**Goal:** Produce deeper semantic findings while preserving a predictable API contract.

Build:

- One OpenAI-compatible provider client using `MODEL_API_KEY`, `MODEL_NAME`, and
  `MODEL_BASE_URL`
- A dedicated analysis instruction that returns the Increment 1 schema
- Request timeout and clear provider-error responses
- A local-analysis fallback when no key is configured
- A visible indicator showing whether the result came from local or model analysis

Tests:

- Provider client tests with mocked HTTP responses
- Invalid JSON and schema-mismatch handling
- Missing-key, timeout, authentication-error, and rate-limit behavior
- No live API calls in the default test suite

**Completion check:** With a key configured, the application returns schema-valid model findings;
without a key, the current local analyzer continues to work.

## Increment 3 — Combine deterministic and semantic analysis

**Goal:** Make findings more reliable than either rules or a model alone.

Build:

- An orchestration step that runs deterministic checks and model analysis
- Deduplication based on rubric rule and evidence span
- Finding provenance: deterministic, model, or both
- Severity definitions with consistent user-facing language
- Detection of contradictions and instructions that could cause scope expansion

Tests:

- Merge and deduplication tests
- Contradictory-instruction fixtures
- Tool mentioned without criteria, permission, or failure handling
- Attempts to classify user content as system-level instructions

**Completion check:** Repeated findings appear once, retain their evidence and provenance, and use
consistent severity levels.

## Increment 4 — Turn results into an interactive prompt map

**Goal:** Let users explore relationships instead of reading a flat report.

Build:

- A graph with the prompt at its center and grouped rule, constraint, guard, tool, and gap nodes
- Edges such as “constrains,” “requires,” “conflicts with,” and “missing from”
- Filters for category, severity, status, and provenance
- Selection details containing evidence, rationale, and recommendation
- Keyboard navigation, focus states, accessible labels, and a useful list fallback
- Responsive behavior for desktop and narrow screens

Tests:

- Browser tests for submitting, filtering, and selecting findings
- Accessibility checks for the main workflow
- Layout smoke tests at desktop and mobile widths

**Completion check:** A user can isolate tool-use gaps, trace each gap back to related instructions,
and use the full workflow with a keyboard.

## Increment 5 — Guided prompt improvement

**Goal:** Help users close gaps without taking control of their prompt.

Build:

- A proposed instruction for each actionable gap
- Accept, edit, or dismiss controls for individual proposals
- A side-by-side original and revised prompt view
- A textual change summary explaining what was added and why
- Re-run analysis against the revised draft
- Copy and download actions; no automatic overwrite of submitted text

Tests:

- Accept, edit, dismiss, and undo behavior
- Original prompt remains unchanged until the user accepts a proposal
- Re-analysis uses the revised draft
- Safe rendering of prompt text and model-produced content

**Completion check:** A user can resolve selected gaps, understand every change, and export a
revised prompt without losing the original.

## Increment 6 — Build an evaluation harness

**Goal:** Measure analysis quality and catch regressions before changing models or instructions.

Build:

- A curated evaluation dataset with expected rubric findings
- Precision and recall reporting by category
- False-positive and false-negative review output
- Latency and estimated model-cost reporting
- A command for comparing two analyzer configurations

Tests:

- Deterministic evaluation runner tests
- Threshold checks for critical categories such as tool permissions and scope boundaries
- Regression fixtures for every confirmed analysis bug

**Completion check:** Analyzer changes can be compared against a baseline, and releases fail when
critical-category quality drops below an agreed threshold.

## Increment 7 — Production hardening

**Goal:** Make the single-user application safe and observable when deployed.

Build:

- Request-size and concurrency limits
- Redacted structured logging with request IDs
- Health, readiness, and provider-connectivity checks
- Secure headers and documented deployment configuration
- Container image and continuous integration for tests and linting
- Explicit retention policy; default remains no prompt persistence

Tests:

- Oversized request and concurrency behavior
- Logs never contain API keys or submitted prompt bodies
- Container startup and health checks
- Dependency and configuration validation in CI

**Completion check:** The service can be deployed reproducibly, failures are diagnosable, and
sensitive prompt content is absent from logs.

## Later, only when usage justifies it

- Saved analyses and prompt version history
- Authentication and team workspaces
- Comments, review links, and collaboration
- Additional model providers
- Organization-specific policy packs and custom rubric rules
- Batch analysis and repository integrations
- Usage analytics and billing

These are intentionally outside the initial roadmap. They add data ownership, security, and
operational complexity that should be driven by observed demand.

## Recommended release boundaries

- **MVP:** Increments 0–3 — dependable structured analysis
- **Useful beta:** Increments 4–5 — interactive exploration and guided improvement
- **Production candidate:** Increments 6–7 — measured quality and operational safeguards

## Working method for every increment

1. Write or update acceptance examples.
2. Add the narrowest failing automated test.
3. Implement the smallest end-to-end behavior.
4. Run unit, API, and relevant browser checks.
5. Review security and privacy impact.
6. Update this plan and the README with the delivered behavior.
7. Stop and demo before beginning the next increment.
