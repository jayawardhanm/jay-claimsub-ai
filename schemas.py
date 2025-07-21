from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClaimBase(BaseModel):
    claim_id: str
    provider_id: str
    risk_id: str
    summary: Optional[str] = None
    status: str
    reason_code: Optional[str]
    reason_description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class ClaimProcessRequest(BaseModel):
    claim_id: str

class ClaimProcessResponse(ClaimBase):
    pass