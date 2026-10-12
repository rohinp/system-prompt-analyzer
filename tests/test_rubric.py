from pathlib import Path

import pytest
from pydantic import ValidationError

from system_prompt_analyzer.analyzer import analyze_prompt
from system_prompt_analyzer.rubric import RUBRIC_RULES, RUBRIC_VERSION
from system_prompt_analyzer.schemas import (
    Evidence,
    Finding,
    FindingSeverity,
    FindingStatus,
    RubricCategory,
)

FIXTURES = Path(__file__).parent / "fixtures" / "prompts"


def finding_for(prompt: str, rule_id: str) -> Finding:
    return next(
        finding for finding in analyze_prompt(prompt).findings if finding.rule_id == rule_id
    )


def test_rubric_has_unique_stable_rule_ids() -> None:
    rule_ids = [rule.id for rule in RUBRIC_RULES]

    assert len(rule_ids) == len(set(rule_ids))
    assert all(rule_id == rule_id.upper() for rule_id in rule_ids)


def test_present_finding_requires_evidence() -> None:
    with pytest.raises(ValidationError, match="present findings must include evidence"):
        Finding(
            id="finding-role-001",
            rule_id="ROLE-001",
            category=RubricCategory.ROLE_OBJECTIVE,
            severity=FindingSeverity.HIGH,
            status=FindingStatus.PRESENT,
            title="Role and objective",
            rationale="A role was detected.",
        )


def test_missing_finding_requires_recommendation() -> None:
    with pytest.raises(ValidationError, match="missing findings must include a recommendation"):
        Finding(
            id="finding-role-001",
            rule_id="ROLE-001",
            category=RubricCategory.ROLE_OBJECTIVE,
            severity=FindingSeverity.HIGH,
            status=FindingStatus.MISSING,
            title="Role and objective",
            rationale="No role was detected.",
        )


def test_evidence_line_range_must_be_ordered() -> None:
    with pytest.raises(ValidationError, match="end_line must be greater"):
        Evidence(quote="Example", start_line=2, end_line=1)


def test_strong_prompt_satisfies_all_applicable_rules() -> None:
    prompt = (FIXTURES / "strong.txt").read_text()
    result = analyze_prompt(prompt)

    assert result.rubric_version == RUBRIC_VERSION
    assert result.finding_summary.missing == 0
    assert all(
        finding.evidence
        for finding in result.findings
        if finding.status == FindingStatus.PRESENT
    )


def test_weak_prompt_exposes_core_gaps() -> None:
    prompt = (FIXTURES / "weak.txt").read_text()
    result = analyze_prompt(prompt)
    missing_rule_ids = {
        finding.rule_id
        for finding in result.findings
        if finding.status == FindingStatus.MISSING
    }

    assert {"ROLE-001", "SCOPE-001", "UNCERTAINTY-001", "OUTPUT-001"} <= missing_rule_ids
    assert all(
        finding.recommendation
        for finding in result.findings
        if finding.status == FindingStatus.MISSING
    )


def test_tool_rules_apply_only_when_tools_are_mentioned() -> None:
    tool_prompt = (FIXTURES / "tool-heavy.txt").read_text()

    assert finding_for("You are an editor. Respond with corrected prose.", "TOOL-001").status == (
        FindingStatus.NOT_APPLICABLE
    )
    assert finding_for(tool_prompt, "TOOL-001").status == FindingStatus.MISSING
    assert finding_for(tool_prompt, "TOOL-002").status == FindingStatus.MISSING


def test_finding_ids_are_stable_across_repeated_analysis() -> None:
    prompt = (FIXTURES / "conflicting.txt").read_text()

    first = analyze_prompt(prompt)
    second = analyze_prompt(prompt)

    assert [finding.id for finding in first.findings] == [
        finding.id for finding in second.findings
    ]
