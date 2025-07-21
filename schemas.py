from pydantic import BaseModel

class ClaimProcessRequest(BaseModel):
    claim_id: str