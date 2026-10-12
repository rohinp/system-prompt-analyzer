# Project documentation

This directory is the living knowledge base for System Prompt Analyzer. It explains both how to
use the product and why it works the way it does.

## For users

- [Product concept](product-concept.md) — the problem, idea, and intended outcomes
- [Getting started](getting-started.md) — install, run, configure, and analyze a prompt
- [Understanding results](concepts.md) — rules, findings, evidence, gaps, and severities
- [Privacy and security](privacy-and-security.md) — what data is handled and current safeguards

## For builders

- [Architecture](architecture.md) — components, request flow, and source layout
- [Analysis rubric](analysis-rubric.md) — the versioned evaluation rules
- [API contract](api.md) — endpoints and response semantics
- [Development guide](development.md) — local workflow, tests, and contribution rules
- [Feature status](feature-status.md) — what works now and what remains planned
- [Architecture decisions](decisions/README.md) — important choices and their tradeoffs

## Documentation policy

Documentation changes are part of feature completion. When behavior changes:

1. Update the relevant user and technical pages in the same change.
2. Update `feature-status.md` and `../PLAN.md` when an increment changes state.
3. Update `api.md` before merging a public contract change.
4. Add an architecture decision when a choice is expensive to reverse or changes a boundary.
5. Describe current behavior separately from future plans; do not document aspirations as shipped.

Code and tests are the final authority when documentation and implementation disagree. Treat such
a disagreement as a defect and correct the documentation or code promptly.
