from app.schemas import Claim, ClaimAnalysis, Finding

SUSPICIOUS_TERMS = {"stolen", "missing", "unknown", "cash", "no receipt", "inconsistent"}

def analyze_claim(claim: Claim) -> ClaimAnalysis:
    findings = []
    amount = claim.estimated_loss
    if amount >= 25000:
        severity, route = "high", "senior_adjuster"
    elif amount >= 7500:
        severity, route = "medium", "adjuster_review"
    else:
        severity, route = "low", "standard_review"

    text = f"{claim.description} {' '.join(claim.evidence)}".lower()
    hits = [term for term in SUSPICIOUS_TERMS if term in text]
    for term in hits:
        findings.append(Finding(
            code="RISK_TERM",
            severity="medium",
            message=f"Risk signal detected: {term}",
            evidence_refs=claim.evidence,
        ))

    if not claim.evidence:
        findings.append(Finding(
            code="MISSING_EVIDENCE",
            severity="high",
            message="No supporting evidence was attached to the claim.",
        ))

    risk_score = min(100.0, len(hits) * 15 + (20 if not claim.evidence else 0) + (15 if amount >= 25000 else 0))
    human_review = bool(findings) or severity == "high"
    return ClaimAnalysis(
        claim_id=claim.id,
        severity=severity,
        route=route,
        risk_score=risk_score,
        human_review_required=human_review,
        findings=findings,
    )
