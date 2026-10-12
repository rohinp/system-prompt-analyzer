# Analysis rubric

Current rubric version: **1.0.0**

The executable definition lives in `src/system_prompt_analyzer/rubric.py` and is exposed through
`GET /api/rubric`. This page explains the human meaning of each rule.

## Applicability

- `always`: evaluated for every prompt
- `when_tools_are_used`: activated by tool, function, API, connector, browser, or command language
- `when_external_actions_are_allowed`: activated by actions such as sending, publishing,
  purchasing, deleting, submitting, posting, messaging, booking, or scheduling
- `when_sensitive_data_is_handled`: activated by sensitive-data language such as secrets,
  passwords, API keys, private or personal data, or medical and financial information

Contextual rules return `not_applicable` when their activation context is absent. They are not
counted as gaps.

## Version 1.0 rules

| ID | Category | Severity if missing | Applies | Requirement |
| --- | --- | --- | --- | --- |
| `ROLE-001` | Role and objective | High | Always | Identify the agent's role or responsible outcome. |
| `SCOPE-001` | Scope boundaries | High | Always | State a boundary, non-goal, or limit on autonomy. |
| `PRIORITY-001` | Instruction priority | Medium | Always | Explain how conflicting instructions are resolved. |
| `TOOL-001` | Tool use | High | Tools used | Define when a named tool should or should not be used. |
| `TOOL-002` | Failure and recovery | High | Tools used | Define behavior when a tool fails or returns bad data. |
| `PERMISSION-001` | Permissions | High | External actions | Require confirmation before consequential actions. |
| `SAFETY-001` | Safety and privacy | High | Sensitive data | Constrain how sensitive data may be handled. |
| `UNCERTAINTY-001` | Uncertainty | Medium | Always | Define behavior for missing or ambiguous information. |
| `OUTPUT-001` | Output contract | Medium | Always | Define response shape, content, or style. |
| `COMPLETION-001` | Output contract | Medium | Always | Define success and stopping criteria. |

## Rule details

### ROLE-001 — Role and objective

A prompt should name the role, goal, objective, purpose, or job. This anchors decisions that are
not exhaustively specified elsewhere. A generic instruction such as “help the user” does not
currently satisfy this check.

### SCOPE-001 — Scope boundaries

A useful boundary states something the agent must not do, limits it to a defined scope, or requires
permission before expansion. Boundaries reduce the risk of the agent doing more than requested.

### PRIORITY-001 — Conflict and priority handling

The prompt should explain which instructions take precedence and what happens when a conflict
cannot be resolved. Version 1.0 detects the presence of conflict-handling language; it does not yet
detect contradictory instructions. Contradiction detection belongs to roadmap Increment 3.

### TOOL-001 — Tool-use criteria

Naming a tool is not enough. The prompt should connect tool language to conditions such as “when,”
“if,” “only,” or “unless.” A model-backed analyzer will later evaluate whether those conditions are
actually sufficient for each tool.

### TOOL-002 — Tool failure behavior

Tool-using agents need bounded retry, fallback, and disclosure behavior. Without it they may retry
indefinitely, conceal failure, or substitute unsupported content.

### PERMISSION-001 — Permission before consequential actions

When a prompt allows sending, publishing, purchasing, deleting, submitting, posting, messaging,
booking, or scheduling, it should preserve user control through explicit approval requirements.
Application code must still enforce permissions; prompt text alone is not an authorization system.

### SAFETY-001 — Sensitive-data handling

When sensitive data is in scope, the prompt should state limits on revelation, sharing, storage,
logging, or inclusion in output. Runtime redaction and access controls remain necessary.

### UNCERTAINTY-001 — Uncertainty and clarification

The agent should know when to ask a question, state an assumption, or explain missing information
instead of inventing details.

### OUTPUT-001 — Output contract

The prompt should describe expected response format, required content, or important exclusions.
This improves consistency and makes downstream validation possible.

### COMPLETION-001 — Completion criteria

The prompt should define how the agent knows the work is complete and what it must verify before
claiming success.

## Versioning rules

The rubric follows semantic versioning in spirit:

- Patch: wording or pattern correction that does not intentionally change rule meaning
- Minor: backward-compatible rule addition
- Major: removed rule, changed rule meaning, changed severity, or changed applicability semantics

Every stored or displayed result must include `rubric_version`.

## Current limitations

The current analyzer is deliberately deterministic and transparent. It uses regular-expression
matches on individual meaningful lines. As a result:

- it can miss valid paraphrases;
- it can accept superficial wording that does not fully satisfy the intent;
- it does not understand relationships across distant sections;
- it does not yet detect contradictions or duplicated rules;
- it does not assess whether tools and permissions are enforced by application code;
- it is currently optimized for English-language prompts.

These limitations are why findings are recommendations rather than guarantees. The next roadmap
increments add semantic model analysis and then combine both sources.
