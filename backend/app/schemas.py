from typing import Dict, List
from pydantic import BaseModel, Field

class Claim(BaseModel):
    id: str
    policy_id: str
    claimant: str
    claim_type: str
    description: str
    estimated_loss: float = Field(ge=0)
    location: str | None = None
    evidence: List[str] = []

class Finding(BaseModel):
    code: str
    severity: str
    message: str
    evidence_refs: List[str] = []

class ClaimAnalysis(BaseModel):
    claim_id: str
    severity: str
    route: str
    risk_score: float
    human_review_required: bool
    findings: List[Finding]
