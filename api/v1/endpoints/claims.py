from fastapi import APIRouter, Depends, HTTPException
from schemas import ClaimProcessRequest
from services.claim_processor import process_claim, process_pending_claims
from core.security import api_key_auth
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/process")
def process_new_claim(request: ClaimProcessRequest, api_key: str = Depends(api_key_auth)):
    try:
        logger.info(f"Processing claim: {request.claim_id}")
        claim = process_claim(request.claim_id)
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        return claim
    except Exception as e:
        logger.error(f"Error processing claim {request.claim_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing claim: {str(e)}")

@router.post("/process-pending")
def batch_process_pending_claims(api_key: str = Depends(api_key_auth)):
    try:
        claims = process_pending_claims()
        return claims
    except Exception as e:
        logger.error(f"Error processing pending claims: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing pending claims: {str(e)}")

@router.get("/test")
def test_endpoint():
    """Test endpoint that doesn't require authentication"""
    return {
        "message": "Claims API is working!",
        "timestamp": "2025-07-20",
        "endpoints": [
            "POST /api/v1/claims/process - Process a single claim",
            "POST /api/v1/claims/process-pending - Process all pending claims",
            "GET /api/v1/claims/test - This test endpoint"
        ]
    }