from services.backend_client import get_claim, update_claim, get_provider, get_risk, get_pending_claims
from services.ai_service import assess_risk, decide_claim

def process_claim(claim_id: str):
    claim = get_claim(claim_id)
    provider = get_provider(claim["provider_id"])
    risk = get_risk(claim["risk_id"])
    score = assess_risk(claim, provider, risk)
    status, reason_code, reason_description = decide_claim(score, claim, provider, risk)
    update_data = {
        "status": status,
        "reason_code": reason_code,
        "reason_description": reason_description
    }
    updated_claim = update_claim(claim_id, update_data)
    return updated_claim

def process_pending_claims():
    pending_claims = get_pending_claims()
    results = []
    for claim in pending_claims:
        provider = get_provider(claim["provider_id"])
        risk = get_risk(claim["risk_id"])
        score = assess_risk(claim, provider, risk)
        status, reason_code, reason_description = decide_claim(score, claim, provider, risk)
        update_data = {
            "status": status,
            "reason_code": reason_code,
            "reason_description": reason_description
        }
        updated_claim = update_claim(claim["claim_id"], update_data)
        results.append(updated_claim)
    return results