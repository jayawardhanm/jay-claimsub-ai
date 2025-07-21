from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import ClaimProcessRequest, ClaimProcessResponse
from app.database import SessionLocal
from app.services.claim_processor import process_claim, process_pending_claims
from app.core.security import api_key_auth

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/process", response_model=ClaimProcessResponse)
def process_new_claim(request: ClaimProcessRequest, db: Session = Depends(get_db), api_key: str = Depends(api_key_auth)):
    claim = process_claim(request.claim_id, db)
    if not claim:
        return {"error": "Claim not found"}
    return claim

@router.post("/process-pending")
def batch_process_pending_claims(db: Session = Depends(get_db), api_key: str = Depends(api_key_auth)):
    claims = process_pending_claims(db)
    return [c for c in claims]