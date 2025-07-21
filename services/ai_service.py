from app.core.config import settings

REASON_CODES = {
    "AUTO_APPR": "Automatically approved - low risk routine treatment",
    "HIGH_RISK_PROVIDER": "Provider flagged for unusual claim patterns",
    "AMOUNT_EXCEEDED": "Claim amount exceeds typical range for procedure",
    "FRAUD_SUSPECTED": "Multiple claims detected, potential fraud",
    "MANUAL_REVIEW": "Requires manual review due to medium risk factors",
    "DOC_REQUIRED": "Additional documentation required"
}

def assess_risk(claim, provider, risk) -> float:
    score = 0.0
    if risk.get("risk_level") == "high":
        score += 0.8
    elif risk.get("risk_level") == "medium":
        score += 0.5
    else:
        score += 0.2

    # Increase score for high amount claims
    try:
        if claim.get("summary") and "amount" in claim["summary"]:
            amount = float(claim["summary"].split("amount:")[1].split()[0])
            if amount > settings.AUTO_APPROVE_AMOUNT:
                score += 0.3
    except Exception:
        pass

    # Provider location risk
    if provider.get("location") in ["fraud_city", "unknown"]:
        score += 0.2

    return min(score, 1.0)

def decide_claim(score, claim, provider, risk):
    summary = claim.get("summary") or ""
    if score < settings.AUTO_APPROVE_THRESHOLD and "amount:" in summary:
        amount = float(summary.split("amount:")[1].split()[0])
        if amount <= settings.AUTO_APPROVE_AMOUNT:
            return "Approved", "AUTO_APPR", REASON_CODES["AUTO_APPR"]
    if score >= settings.AUTO_DENY_THRESHOLD:
        if risk.get("risk_level") == "high":
            return "Denied", "HIGH_RISK_PROVIDER", REASON_CODES["HIGH_RISK_PROVIDER"]
        return "Denied", "FRAUD_SUSPECTED", REASON_CODES["FRAUD_SUSPECTED"]
    if score >= settings.RISK_MEDIUM:
        return "Pending", "MANUAL_REVIEW", REASON_CODES["MANUAL_REVIEW"]
    if score < settings.RISK_LOW:
        return "Approved", "AUTO_APPR", REASON_CODES["AUTO_APPR"]
    return "Pending", "DOC_REQUIRED", REASON_CODES["DOC_REQUIRED"]