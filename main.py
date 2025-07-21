from fastapi import FastAPI
from api.v1.endpoints.claims import router as claims_router
from core.config import settings
from database import engine, Base

app = FastAPI(
    title="Insurance Claim AI Service",
    version="1.0.0",
)

# Create DB tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(claims_router, prefix="/api/v1/claims", tags=["Claims"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "database": True}