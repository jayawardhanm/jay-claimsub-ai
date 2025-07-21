from services.backend_client import get_claim, update_claim, get_provider, get_risk, get_pending_claims
from services.ai_service import assess_risk, decide_claim, process_claim_with_ai
from core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_data_sources(claim_id):
    """Get claim data from real backend only"""
    logger.info(f"Getting real backend data for claim {claim_id}")
    claim = get_claim(claim_id)
    provider = get_provider(claim["provider_id"])
    risk = get_risk(claim["risk_id"])
    return claim, provider, risk

def update_claim_data(claim_id, update_data):
    """Update claim data in real backend"""
    return update_claim(claim_id, update_data)

def process_claim(claim_id: str):
    claim, provider, risk = get_data_sources(claim_id)
    
    # Use AI-powered assessment only
    ai_result = process_claim_with_ai(claim, provider, risk)
    update_data = {
        "status": ai_result["decision"],
        "reason_code": ai_result["reason_code"],
        "reason_description": ai_result["reason_description"],
        "confidence_score": ai_result["confidence_score"],
        "ai_analysis": ai_result.get("analysis", ""),
        "risk_factors": ai_result.get("risk_factors", [])
    }
    
    updated_claim = update_claim_data(claim_id, update_data)
    return updated_claim

def process_pending_claims():
    logger.info("Getting pending claims from real backend")
    pending_claims = get_pending_claims()
    
    results = []
    for claim in pending_claims:
        provider = get_provider(claim["provider_id"])
        risk = get_risk(claim["risk_id"])
        
        # Use AI-powered assessment only
        ai_result = process_claim_with_ai(claim, provider, risk)
        update_data = {
            "status": ai_result["decision"],
            "reason_code": ai_result["reason_code"],
            "reason_description": ai_result["reason_description"],
            "confidence_score": ai_result["confidence_score"],
            "ai_analysis": ai_result.get("analysis", ""),
            "risk_factors": ai_result.get("risk_factors", [])
        }
            
        updated_claim = update_claim_data(claim["claim_id"], update_data)
        results.append(updated_claim)
    return results