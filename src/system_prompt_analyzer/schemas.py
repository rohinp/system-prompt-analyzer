from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class RubricCategory(StrEnum):
    ROLE_OBJECTIVE = "role_objective"
    SCOPE_BOUNDARIES = "scope_boundaries"
    INSTRUCTION_PRIORITY = "instruction_priority"
    TOOL_USE = "tool_use"
    PERMISSIONS = "permissions"
    SAFETY_PRIVACY = "safety_privacy"
    UNCERTAINTY = "uncertainty"
    OUTPUT_CONTRACT = "output_contract"
    FAILURE_RECOVERY = "failure_recovery"


class FindingSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FindingStatus(StrEnum):
    PRESENT = "present"
    MISSING = "missing"
    NOT_APPLICABLE = "not_applicable"


class FindingProvenance(StrEnum):
    DETERMINISTIC = "deterministic"
    MODEL = "model"
    BOTH = "both"


class NodeKind(StrEnum):
    INSTRUCTION = "instruction"
    CONSTRAINT = "constraint"
    GUARD = "guard"
    TOOL = "tool"
    GAP = "gap"


class NodeStatus(StrEnum):
    PRESENT = "present"
    SUGGESTED = "suggested"


class PromptNode(BaseModel):
    id: str
    title: str
    detail: str
    kind: NodeKind
    status: NodeStatus
    evidence: str | None = None
    rule_id: str | None = None


class PromptEdge(BaseModel):
    source: str
    target: str
    label: str


class Evidence(BaseModel):
    quote: str = Field(min_length=1)
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_line_order(self) -> "Evidence":
        if self.end_line < self.start_line:
            raise ValueError("end_line must be greater than or equal to start_line")
        return self


class Finding(BaseModel):
    id: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    category: RubricCategory
    severity: FindingSeverity
    status: FindingStatus
    title: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    evidence: list[Evidence] = Field(default_factory=list)
    recommendation: str | None = None
    provenance: FindingProvenance = FindingProvenance.DETERMINISTIC

    @model_validator(mode="after")
    def validate_status_fields(self) -> "Finding":
        if self.status == FindingStatus.PRESENT and not self.evidence:
            raise ValueError("present findings must include evidence")
        if self.status == FindingStatus.MISSING and not self.recommendation:
            raise ValueError("missing findings must include a recommendation")
        return self


class FindingSummary(BaseModel):
    present: int = Field(ge=0)
    missing: int = Field(ge=0)
    not_applicable: int = Field(ge=0)


class RubricRuleResponse(BaseModel):
    id: str
    category: RubricCategory
    title: str
    description: str
    why_it_matters: str
    severity_when_missing: FindingSeverity
    recommendation: str
    applicability: str


class RubricResponse(BaseModel):
    version: str
    rules: list[RubricRuleResponse]


class AnalyzeRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=50_000)


class AnalyzeResponse(BaseModel):
    analysis_version: str
    rubric_version: str
    summary: str
    finding_summary: FindingSummary
    findings: list[Finding]
    nodes: list[PromptNode]
    edges: list[PromptEdge]


class RuntimeConfigResponse(BaseModel):
    provider: str
    model: str
    api_key_configured: bool
