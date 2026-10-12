# Core concepts

## System prompt

The instruction text being evaluated. The analyzer treats the submitted text as data; instructions
inside it do not control the analyzer itself.

## Rubric

A named, versioned collection of rules describing useful controls in a system prompt. Versioning
allows the meaning of an analysis to remain clear after rules evolve.

## Rule

One review criterion with a stable ID such as `TOOL-001`. A rule defines:

- category and title
- what good coverage means
- why it matters
- when it applies
- severity when missing
- a recommended improvement
- deterministic evidence patterns used by the current analyzer

## Finding

The result of applying one rubric rule to one prompt. Exactly one finding is returned per rule.
Its stable ID is derived from the rule, for example `finding-tool-001`.

## Finding status

| Status | Meaning |
| --- | --- |
| `present` | The rule applies and matching evidence was detected. |
| `missing` | The rule applies, but matching evidence was not detected. |
| `not_applicable` | The prompt lacks the context that activates this rule. |

“Present” means the current analyzer found textual evidence. It does not yet prove that the
instruction is complete, internally consistent, or operationally enforceable.

## Evidence

A verbatim prompt excerpt with inclusive, one-based `start_line` and `end_line` numbers. Present
findings must contain evidence. Missing findings contain no fabricated evidence.

## Severity

Severity describes the likely impact of a missing control, not the quality of wording:

- `high`: absence can materially change scope, safety, permissions, or tool behavior.
- `medium`: absence can reduce predictability, consistency, or completion quality.
- `low`: absence is primarily a clarity or maintainability concern.

Version 1.0 contains high- and medium-severity rules. The `low` value is reserved by the contract
for future rubric additions.

## Provenance

Provenance identifies how a finding was produced:

- `deterministic`: produced by local explicit checks
- `model`: produced by a future semantic analyzer
- `both`: independently supported by both analyzers

All current findings use `deterministic`.

## Statement node

A visual representation of a meaningful prompt line. It may be classified as an instruction,
constraint, guard, or tool statement. This classification supports exploration and is separate
from formal rubric findings.

## Gap node

A visual representation of a missing finding. It carries the originating `rule_id` so it can be
traced back to the rubric definition.

## Response version versus rubric version

- `analysis_version` versions the structure and semantics of the analysis response.
- `rubric_version` versions the rules used to produce findings.

They are independent because the API shape may change without changing the rubric, and rubric
rules may change without requiring a new response shape.
