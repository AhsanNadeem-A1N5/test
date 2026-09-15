from app.schemas import Claim, ClaimAnalysis, RiskSignal

SUSPICIOUS_TERMS = ("staged", "fake", "altered", "duplicate", "cash only")


def analyze_claim(claim: Claim) -> ClaimAnalysis:
    amount = claim.claimed_amount
    severity = "low" if amount < 7500 else "medium" if amount < 25000 else "high"
    route = "standard_review" if severity == "low" else "senior_adjuster" if severity == "medium" else "specialist_review"

    text = f"{claim.description}".lower()
    signals: list[RiskSignal] = []
    for term in SUSPICIOUS_TERMS:
        if term in text:
            signals.append(RiskSignal(
                code=f"TERM_{term.upper().replace(' ', '_')}",
                severity="medium",
                explanation=f"Claim narrative contains the review signal '{term}'."
            ))

    if claim.evidence_count == 0:
        signals.append(RiskSignal(
            code="NO_EVIDENCE",
            severity="high",
            explanation="No supporting evidence has been attached to the claim."
        ))

    human_review = severity != "low" or bool(signals)
    rationale = [
        f"Claim amount ${amount:,.2f} maps to {severity} severity.",
        f"Routing policy selected '{route}'.",
        f"Evidence count: {claim.evidence_count}.",
    ]
    return ClaimAnalysis(
        claim_id=claim.id,
        severity=severity,
        route=route,
        human_review_required=human_review,
        risk_signals=signals,
        rationale=rationale,
    )
