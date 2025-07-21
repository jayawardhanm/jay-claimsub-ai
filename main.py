from fastapi import FastAPI
from api.v1.endpoints.claims import router as claims_router

app = FastAPI(
    title="Insurance Claim AI Service (API backend mode)",
    version="1.0.0",
)

app.include_router(claims_router, prefix="/api/v1/claims", tags=["Claims"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}