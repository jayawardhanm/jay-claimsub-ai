from services.backend_client import (
    get_claim, update_claim, get_provider, get_risk, get_pending_claims,
    get_patient, get_insurance_policy, get_claim_riders
)
from services.ai_service import assess_risk, decide_claim, process_claim_with_ai
from core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_comprehensive_claim_data(claim_id):
    """Get comprehensive claim data including all related entities"""
    logger.info(f"Getting comprehensive data for claim {claim_id}")
    
    # Get base claim data
    claim = get_claim(claim_id)
    
    # Get related entities
    provider = get_provider(claim["provider_id"])
    risk = get_risk(claim["risk_id"])
    
    # Get new comprehensive data
    patient = None
    policy = None
    riders = []
    
    try:
        if claim.get("patient_id"):
            patient = get_patient(claim["patient_id"])
    except Exception as e:
        logger.warning(f"Could not retrieve patient data: {str(e)}")
    
    try:
        if claim.get("policy_id"):
            policy = get_insurance_policy(claim["policy_id"])
    except Exception as e:
        logger.warning(f"Could not retrieve policy data: {str(e)}")
    
    try:
        riders = get_claim_riders(claim_id)
    except Exception as e:
        logger.warning(f"Could not retrieve claim riders: {str(e)}")
    
    return {
        "claim": claim,
        "provider": provider,
        "risk": risk,
        "patient": patient,
        "policy": policy,
        "riders": riders
    }

def get_data_sources(claim_id):
    """Get claim data from real backend only - backwards compatibility"""
    logger.info(f"Getting real backend data for claim {claim_id}")
    claim = get_claim(claim_id)
    provider = get_provider(claim["provider_id"])
    risk = get_risk(claim["risk_id"])
    return claim, provider, risk

def update_claim_data(claim_id, update_data):
    """Update claim data in real backend"""
    return update_claim(claim_id, update_data)

def process_claim(claim_id: str):
    """Process a claim with comprehensive analysis using all available data"""
    comprehensive_data = get_comprehensive_claim_data(claim_id)
    
    # Use AI-powered assessment with comprehensive data
    ai_result = process_claim_with_ai(comprehensive_data)
    
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
    """Process all pending claims with comprehensive analysis"""
    logger.info("Getting pending claims from real backend")
    pending_claims = get_pending_claims()
    
    results = []
    for claim in pending_claims:
        try:
            # Get comprehensive data for each claim
            comprehensive_data = get_comprehensive_claim_data(claim["claim_id"])
            
            # Use AI-powered assessment with comprehensive data
            ai_result = process_claim_with_ai(comprehensive_data)
            
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
        except Exception as e:
            logger.error(f"Error processing claim {claim.get('claim_id', 'unknown')}: {str(e)}")
            # Continue with other claims even if one fails
            continue
    
    return results