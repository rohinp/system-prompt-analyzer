# ADR-0001: Use a versioned executable rubric

- Status: Accepted
- Date: 2026-10-12

## Context

Free-form model feedback is difficult to test, compare, visualize, and explain. The product needs
a stable meaning for “gap” before a model is added.

## Decision

Define rubric rules as executable application data with stable IDs and a semantic version. Return
exactly one structured finding per rule and expose the public rule definition through the API.

Keep visual nodes as a projection of findings rather than the primary analysis contract.

## Consequences

- Deterministic and future model analyzers share one vocabulary.
- Tests can protect evidence, status, and recommendation invariants.
- Historical results can identify the rubric that produced them.
- Changing rule meaning requires deliberate version management.
- Pattern matching remains limited until semantic analysis is added.
