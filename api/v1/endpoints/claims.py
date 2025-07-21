from fastapi import APIRouter, Depends
from schemas import ClaimProcessRequest
from services.claim_processor import process_claim, process_pending_claims
from core.security import api_key_auth

router = APIRouter()

@router.post("/process")
def process_new_claim(request: ClaimProcessRequest, api_key: str = Depends(api_key_auth)):
    claim = process_claim(request.claim_id)
    if not claim:
        return {"error": "Claim not found"}
    return claim

@router.post("/process-pending")
def batch_process_pending_claims(api_key: str = Depends(api_key_auth)):
    claims = process_pending_claims()
    return claims