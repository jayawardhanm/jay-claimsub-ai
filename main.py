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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)