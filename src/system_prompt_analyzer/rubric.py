from dataclasses import dataclass
from enum import StrEnum

from .schemas import FindingSeverity, RubricCategory, RubricResponse, RubricRuleResponse

RUBRIC_VERSION = "1.0.0"
ANALYSIS_VERSION = "1.0.0"


class Applicability(StrEnum):
    ALWAYS = "always"
    WHEN_TOOLS_ARE_USED = "when_tools_are_used"
    WHEN_EXTERNAL_ACTIONS_ARE_ALLOWED = "when_external_actions_are_allowed"
    WHEN_SENSITIVE_DATA_IS_HANDLED = "when_sensitive_data_is_handled"


@dataclass(frozen=True)
class RubricRule:
    id: str
    category: RubricCategory
    title: str
    description: str
    why_it_matters: str
    severity_when_missing: FindingSeverity
    recommendation: str
    applicability: Applicability
    present_patterns: tuple[str, ...]


RUBRIC_RULES = (
    RubricRule(
        id="ROLE-001",
        category=RubricCategory.ROLE_OBJECTIVE,
        title="Role and objective",
        description="The prompt identifies the agent's role or the outcome it is responsible for.",
        why_it_matters="A clear purpose anchors later decisions and reduces irrelevant behavior.",
        severity_when_missing=FindingSeverity.HIGH,
        recommendation="State who the agent is and the primary outcome it should achieve.",
        applicability=Applicability.ALWAYS,
        present_patterns=(
            r"\byou are\b",
            r"\byour (role|goal|objective|purpose|job)\b",
            r"\b(goal|objective|purpose) is\b",
            r"\bact as\b",
        ),
    ),
    RubricRule(
        id="SCOPE-001",
        category=RubricCategory.SCOPE_BOUNDARIES,
        title="Scope boundaries",
        description="The prompt states at least one boundary, non-goal, or limit on autonomy.",
        why_it_matters="Without a boundary, an agent may expand the task beyond user intent.",
        severity_when_missing=FindingSeverity.HIGH,
        recommendation=(
            "State what is out of scope and when the agent must ask before expanding the task."
        ),
        applicability=Applicability.ALWAYS,
        present_patterns=(
            r"\bdo not\b",
            r"\bmust not\b",
            r"\bnever\b",
            r"\bonly\b",
            r"\bout of scope\b",
            r"\bwithout (explicit )?(permission|approval)\b",
        ),
    ),
    RubricRule(
        id="PRIORITY-001",
        category=RubricCategory.INSTRUCTION_PRIORITY,
        title="Conflict and priority handling",
        description="The prompt explains how to resolve conflicting or competing instructions.",
        why_it_matters=(
            "An explicit priority rule makes behavior predictable when directions clash."
        ),
        severity_when_missing=FindingSeverity.MEDIUM,
        recommendation=(
            "Define which instructions take precedence and what to do when a conflict remains."
        ),
        applicability=Applicability.ALWAYS,
        present_patterns=(
            r"\bin case of (a )?conflict\b",
            r"\bif instructions conflict\b",
            r"\b(higher|lower) priority\b",
            r"\btakes? precedence\b",
            r"\binstruction hierarchy\b",
        ),
    ),
    RubricRule(
        id="TOOL-001",
        category=RubricCategory.TOOL_USE,
        title="Tool-use criteria",
        description="The prompt defines when a named tool should or should not be used.",
        why_it_matters="A tool name alone does not define the conditions for invoking it.",
        severity_when_missing=FindingSeverity.HIGH,
        recommendation=(
            "For each tool, state its purpose, invocation conditions, and when not to use it."
        ),
        applicability=Applicability.WHEN_TOOLS_ARE_USED,
        present_patterns=(
            r"\b(tool|function|api|connector|browser|command)\b[^.\n]*(when|if|only|unless)",
            r"\b(when|if|only|unless)\b[^.\n]*(tool|function|api|connector|browser|command)\b",
        ),
    ),
    RubricRule(
        id="TOOL-002",
        category=RubricCategory.FAILURE_RECOVERY,
        title="Tool failure behavior",
        description="The prompt defines what to do when a tool call fails or returns bad data.",
        why_it_matters=(
            "Unspecified failure behavior can cause loops, fabricated results, or drift."
        ),
        severity_when_missing=FindingSeverity.HIGH,
        recommendation=(
            "Define retry limits, fallback behavior, and when to report the failure to the user."
        ),
        applicability=Applicability.WHEN_TOOLS_ARE_USED,
        present_patterns=(
            r"\b(tool|function|api|connector|browser|command)\b[^.\n]*(fail|error|unavailable)",
            r"\b(fail|error|unavailable)\b[^.\n]*(retry|fallback|tool|user)",
        ),
    ),
    RubricRule(
        id="PERMISSION-001",
        category=RubricCategory.PERMISSIONS,
        title="Permission before consequential actions",
        description="The prompt requires confirmation before external or irreversible actions.",
        why_it_matters="Consequential actions should remain under deliberate user control.",
        severity_when_missing=FindingSeverity.HIGH,
        recommendation=(
            "Require explicit user approval before sending, publishing, purchasing, or deleting."
        ),
        applicability=Applicability.WHEN_EXTERNAL_ACTIONS_ARE_ALLOWED,
        present_patterns=(
            r"\b(ask|require|get|obtain|confirm)\b[^.\n]*(permission|approval|confirmation)",
            r"\bdo not\b[^.\n]*(send|publish|purchase|delete|submit|post)\b[^.\n]*\buntil\b",
        ),
    ),
    RubricRule(
        id="SAFETY-001",
        category=RubricCategory.SAFETY_PRIVACY,
        title="Sensitive-data handling",
        description="The prompt constrains how secrets or sensitive user data may be handled.",
        why_it_matters="Explicit handling rules reduce accidental disclosure or retention.",
        severity_when_missing=FindingSeverity.HIGH,
        recommendation=(
            "State how sensitive data must be minimized, protected, and excluded from outputs."
        ),
        applicability=Applicability.WHEN_SENSITIVE_DATA_IS_HANDLED,
        present_patterns=(
            r"\b(do not|never|must not)\b[^.\n]*(reveal|share|expose|store|log)",
            r"\b(redact|minimi[sz]e|protect)\b[^.\n]*(secret|password|key|sensitive|private)",
        ),
    ),
    RubricRule(
        id="UNCERTAINTY-001",
        category=RubricCategory.UNCERTAINTY,
        title="Uncertainty and clarification",
        description="The prompt defines behavior for missing, ambiguous, or uncertain information.",
        why_it_matters="The agent should not invent details or make material assumptions silently.",
        severity_when_missing=FindingSeverity.MEDIUM,
        recommendation=(
            "Tell the agent when to ask a clarifying question and how to label assumptions."
        ),
        applicability=Applicability.ALWAYS,
        present_patterns=(
            r"\b(ask|request)\b[^.\n]*(clarif|more information)",
            r"\b(if|when)\b[^.\n]*(ambiguous|uncertain|missing information|unclear)",
            r"\bstate (your )?assumptions\b",
        ),
    ),
    RubricRule(
        id="OUTPUT-001",
        category=RubricCategory.OUTPUT_CONTRACT,
        title="Output contract",
        description="The prompt defines the shape, content, or style of the final response.",
        why_it_matters="A response contract makes results consistent and easier to consume.",
        severity_when_missing=FindingSeverity.MEDIUM,
        recommendation="Specify the response format, required content, and important exclusions.",
        applicability=Applicability.ALWAYS,
        present_patterns=(
            r"\brespond with\b",
            r"\breturn (only |a |an |the )",
            r"\boutput (format|must|should)\b",
            r"\bformat (the response|as)\b",
            r"\binclude the following\b",
        ),
    ),
    RubricRule(
        id="COMPLETION-001",
        category=RubricCategory.OUTPUT_CONTRACT,
        title="Completion criteria",
        description="The prompt says how the agent can determine that the task is complete.",
        why_it_matters="A stopping condition prevents premature completion or unnecessary work.",
        severity_when_missing=FindingSeverity.MEDIUM,
        recommendation=(
            "Define success criteria and the checks required before reporting completion."
        ),
        applicability=Applicability.ALWAYS,
        present_patterns=(
            r"\b(success|completion) criteria\b",
            r"\b(task|work) is (complete|done) when\b",
            r"\bbefore (finishing|reporting completion)\b",
            r"\bverify that\b",
        ),
    ),
)


def rubric_response() -> RubricResponse:
    return RubricResponse(
        version=RUBRIC_VERSION,
        rules=[
            RubricRuleResponse(
                id=rule.id,
                category=rule.category,
                title=rule.title,
                description=rule.description,
                why_it_matters=rule.why_it_matters,
                severity_when_missing=rule.severity_when_missing,
                recommendation=rule.recommendation,
                applicability=rule.applicability,
            )
            for rule in RUBRIC_RULES
        ],
    )
