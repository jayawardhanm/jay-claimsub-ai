from app.models import Claim, Provider, Risk
from app.services.ai_service import assess_risk, decide_claim
from sqlalchemy.orm import Session

def process_claim(claim_id: str, db: Session):
    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    if not claim:
        return None
    provider = db.query(Provider).filter(Provider.provider_id == claim.provider_id).first()
    risk = db.query(Risk).filter(Risk.risk_id == claim.risk_id).first()
    score = assess_risk(claim, provider, risk, db)
    status, reason_code, reason_desc = decide_claim(score, claim, provider, risk)
    claim.status = status
    claim.reason_code = reason_code
    claim.reason_description = reason_desc
    db.commit()
    db.refresh(claim)
    return claim

def process_pending_claims(db: Session):
    pending_claims = db.query(Claim).filter(Claim.status == "Pending").all()
    results = []
    for claim in pending_claims:
        provider = db.query(Provider).filter(Provider.provider_id == claim.provider_id).first()
        risk = db.query(Risk).filter(Risk.risk_id == claim.risk_id).first()
        score = assess_risk(claim, provider, risk, db)
        status, reason_code, reason_desc = decide_claim(score, claim, provider, risk)
        claim.status = status
        claim.reason_code = reason_code
        claim.reason_description = reason_desc
        db.commit()
        db.refresh(claim)
        results.append(claim)
    return results