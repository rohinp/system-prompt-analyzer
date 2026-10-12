import re
from dataclasses import dataclass

from .rubric import ANALYSIS_VERSION, RUBRIC_RULES, RUBRIC_VERSION, Applicability, RubricRule
from .schemas import (
    AnalyzeResponse,
    Evidence,
    Finding,
    FindingProvenance,
    FindingStatus,
    FindingSummary,
    NodeKind,
    NodeStatus,
    PromptEdge,
    PromptNode,
)

TOOL_PATTERN = re.compile(r"\b(tool|function|api|connector|browser|command)\b", re.IGNORECASE)
EXTERNAL_ACTION_PATTERN = re.compile(
    r"\b(send|publish|purchase|buy|delete|submit|post|message|book|schedule)\b",
    re.IGNORECASE,
)
SENSITIVE_DATA_PATTERN = re.compile(
    r"\b(secret|password|api key|sensitive|private|personal data|medical|financial)\b",
    re.IGNORECASE,
)
CONSTRAINT_PATTERN = re.compile(r"\b(must|never|do not|only|cannot|required)\b", re.IGNORECASE)
GUARD_PATTERN = re.compile(
    r"\b(safety|permission|approval|secret|private|sensitive)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PromptLine:
    number: int
    text: str


def _meaningful_lines(prompt: str) -> list[PromptLine]:
    lines: list[PromptLine] = []
    for number, raw_line in enumerate(prompt.splitlines(), start=1):
        line = raw_line.strip().lstrip("-*#").strip()
        if line:
            lines.append(PromptLine(number=number, text=line))
    return lines


def _is_applicable(rule: RubricRule, prompt: str) -> bool:
    if rule.applicability == Applicability.ALWAYS:
        return True
    if rule.applicability == Applicability.WHEN_TOOLS_ARE_USED:
        return bool(TOOL_PATTERN.search(prompt))
    if rule.applicability == Applicability.WHEN_EXTERNAL_ACTIONS_ARE_ALLOWED:
        return bool(EXTERNAL_ACTION_PATTERN.search(prompt))
    if rule.applicability == Applicability.WHEN_SENSITIVE_DATA_IS_HANDLED:
        return bool(SENSITIVE_DATA_PATTERN.search(prompt))
    return False


def _matching_evidence(rule: RubricRule, lines: list[PromptLine]) -> list[Evidence]:
    evidence: list[Evidence] = []
    for line in lines:
        if any(re.search(pattern, line.text, re.IGNORECASE) for pattern in rule.present_patterns):
            evidence.append(
                Evidence(quote=line.text, start_line=line.number, end_line=line.number)
            )
    return evidence[:3]


def _finding_for(rule: RubricRule, prompt: str, lines: list[PromptLine]) -> Finding:
    finding_id = f"finding-{rule.id.lower()}"
    if not _is_applicable(rule, prompt):
        return Finding(
            id=finding_id,
            rule_id=rule.id,
            category=rule.category,
            severity=rule.severity_when_missing,
            status=FindingStatus.NOT_APPLICABLE,
            title=rule.title,
            rationale=f"This check applies {rule.applicability.value.replace('_', ' ')}.",
            provenance=FindingProvenance.DETERMINISTIC,
        )

    evidence = _matching_evidence(rule, lines)
    if evidence:
        return Finding(
            id=finding_id,
            rule_id=rule.id,
            category=rule.category,
            severity=rule.severity_when_missing,
            status=FindingStatus.PRESENT,
            title=rule.title,
            rationale=rule.why_it_matters,
            evidence=evidence,
            provenance=FindingProvenance.DETERMINISTIC,
        )

    return Finding(
        id=finding_id,
        rule_id=rule.id,
        category=rule.category,
        severity=rule.severity_when_missing,
        status=FindingStatus.MISSING,
        title=rule.title,
        rationale=f"No prompt text was found that satisfies {rule.id}: {rule.description}",
        recommendation=rule.recommendation,
        provenance=FindingProvenance.DETERMINISTIC,
    )


def _node_kind(line: str) -> NodeKind:
    if TOOL_PATTERN.search(line):
        return NodeKind.TOOL
    if GUARD_PATTERN.search(line):
        return NodeKind.GUARD
    if CONSTRAINT_PATTERN.search(line):
        return NodeKind.CONSTRAINT
    return NodeKind.INSTRUCTION


def _prompt_nodes(
    lines: list[PromptLine], word_count: int
) -> tuple[list[PromptNode], list[PromptEdge]]:
    nodes: list[PromptNode] = [
        PromptNode(
            id="prompt",
            title="System prompt",
            detail=f"{word_count} words across {len(lines)} meaningful lines.",
            kind=NodeKind.INSTRUCTION,
            status=NodeStatus.PRESENT,
        )
    ]
    edges: list[PromptEdge] = []

    for line in lines[:12]:
        node_id = f"statement-{line.number}"
        nodes.append(
            PromptNode(
                id=node_id,
                title=line.text[:72] + ("…" if len(line.text) > 72 else ""),
                detail=f"Detected prompt statement on line {line.number}",
                kind=_node_kind(line.text),
                status=NodeStatus.PRESENT,
                evidence=line.text,
            )
        )
        edges.append(PromptEdge(source="prompt", target=node_id, label="contains"))

    return nodes, edges


def analyze_prompt(prompt: str) -> AnalyzeResponse:
    """Evaluate a prompt against the versioned deterministic rubric."""
    lines = _meaningful_lines(prompt)
    findings = [_finding_for(rule, prompt, lines) for rule in RUBRIC_RULES]
    nodes, edges = _prompt_nodes(lines, len(prompt.split()))

    for finding in findings:
        if finding.status != FindingStatus.MISSING:
            continue
        node_id = f"gap-{finding.rule_id.lower()}"
        nodes.append(
            PromptNode(
                id=node_id,
                title=finding.title,
                detail=finding.recommendation or finding.rationale,
                kind=NodeKind.GAP,
                status=NodeStatus.SUGGESTED,
                rule_id=finding.rule_id,
            )
        )
        edges.append(PromptEdge(source="prompt", target=node_id, label="missing"))

    finding_summary = FindingSummary(
        present=sum(finding.status == FindingStatus.PRESENT for finding in findings),
        missing=sum(finding.status == FindingStatus.MISSING for finding in findings),
        not_applicable=sum(
            finding.status == FindingStatus.NOT_APPLICABLE for finding in findings
        ),
    )
    summary = (
        f"Mapped {len(lines)} prompt statements and found "
        f"{finding_summary.missing} rubric gaps."
    )
    return AnalyzeResponse(
        analysis_version=ANALYSIS_VERSION,
        rubric_version=RUBRIC_VERSION,
        summary=summary,
        finding_summary=finding_summary,
        findings=findings,
        nodes=nodes,
        edges=edges,
    )
