# Feature status

Last updated: 2026-10-12

## Available now

- Local FastAPI application and responsive web interface
- Prompt submission up to 50,000 characters
- Rubric version `1.0.0` with ten stable rules across nine categories
- Findings with status, severity, provenance, rationale, recommendation, and line evidence
- Contextual not-applicable handling for tools, external actions, and sensitive data
- Visual statement and gap nodes
- Public rubric and OpenAPI endpoints
- Environment-based model-provider configuration
- Representative strong, weak, tool-heavy, and conflicting prompt fixtures
- Automated schema, rubric, and API tests

## Partially available

- The interface visualizes source statements and missing findings but does not yet expose filters,
  full finding details, or relationship navigation.
- Provider configuration exists, but model API calls are not implemented.
- Conflict-handling instructions are detected, but contradictions inside a prompt are not.

## Planned next

- One OpenAI-compatible model-backed analyzer
- Structured error handling and local fallback
- Analysis-source indicator
- Deterministic and semantic finding merge with provenance

See `../PLAN.md` for the complete incremental roadmap.
