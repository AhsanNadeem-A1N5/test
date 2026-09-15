from fastapi import FastAPI, HTTPException
from app.schemas import Claim, ClaimAnalysis
from app.services.analysis import analyze_claim
from app.services.store import store

app = FastAPI(title="ClaimForge AI", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "claimforge-api"}

@app.post("/claims", response_model=Claim)
def create_claim(claim: Claim):
    if claim.id in store:
        raise HTTPException(status_code=409, detail="Claim already exists")
    store[claim.id] = claim
    return claim

@app.get("/claims/{claim_id}", response_model=Claim)
def get_claim(claim_id: str):
    if claim_id not in store:
        raise HTTPException(status_code=404, detail="Claim not found")
    return store[claim_id]

@app.post("/claims/{claim_id}/analyze", response_model=ClaimAnalysis)
def analyze(claim_id: str):
    claim = store.get(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return analyze_claim(claim)
