# API contract

The FastAPI schema is available at `/openapi.json` and interactive documentation at `/docs`.

## Compatibility policy

The API is pre-1.0 and may evolve, but response semantics are explicitly versioned:

- `analysis_version` identifies analysis response semantics.
- `rubric_version` identifies the evaluation rules.
- rubric rule IDs remain stable within a major rubric version.
- clients should ignore unknown response fields and use enum values defensively.

## `GET /api/health`

Confirms that the application process can serve requests.

```json
{"status": "ok"}
```

This is a liveness check, not a provider-connectivity check.

## `GET /api/config`

Returns safe, public runtime configuration. It never returns the API key.

```json
{
  "provider": "openai",
  "model": "gpt-5-mini",
  "api_key_configured": false
}
```

## `GET /api/rubric`

Returns the rubric version and public definition of every rule. Pattern-matching implementation
details are intentionally excluded from the public response.

Each rule contains:

- `id`
- `category`
- `title`
- `description`
- `why_it_matters`
- `severity_when_missing`
- `recommendation`
- `applicability`

## `POST /api/analyze`

Request:

```json
{
  "prompt": "You are a research assistant. Respond with a concise summary."
}
```

`prompt` must contain between 1 and 50,000 characters.

Response sections:

| Field | Meaning |
| --- | --- |
| `analysis_version` | Version of response semantics |
| `rubric_version` | Rubric version used for evaluation |
| `summary` | Short human-readable result |
| `finding_summary` | Counts by status |
| `findings` | One structured result per rubric rule |
| `nodes` | Visual prompt and gap nodes |
| `edges` | Relationships between visual nodes |

Finding example:

```json
{
  "id": "finding-role-001",
  "rule_id": "ROLE-001",
  "category": "role_objective",
  "severity": "high",
  "status": "present",
  "title": "Role and objective",
  "rationale": "A clear purpose anchors later decisions and reduces irrelevant behavior.",
  "evidence": [
    {
      "quote": "You are a research assistant.",
      "start_line": 1,
      "end_line": 1
    }
  ],
  "recommendation": null,
  "provenance": "deterministic"
}
```

Contract invariants:

- There is exactly one finding for every rule in the referenced rubric version.
- A `present` finding has at least one evidence item.
- A `missing` finding has a recommendation.
- A `not_applicable` finding is not counted as missing.
- Evidence line numbers are one-based and inclusive.
- Gap nodes contain the `rule_id` of their source finding.

Validation errors use FastAPI's standard HTTP `422` response. Provider-specific errors will be
documented when the model-backed increment is implemented.
