from pydantic import BaseModel, Field

class Claim(BaseModel):
    id: str = Field(min_length=1)
    claimant_name: str = Field(min_length=1)
    claim_type: str = Field(min_length=1)
    description: str = Field(min_length=1)
    claimed_amount: float = Field(ge=0)
    evidence_count: int = Field(default=0, ge=0)

class RiskSignal(BaseModel):
    code: str
    severity: str
    explanation: str

class ClaimAnalysis(BaseModel):
    claim_id: str
    severity: str
    route: str
    human_review_required: bool
    risk_signals: list[RiskSignal]
    rationale: list[str]
