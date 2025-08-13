import requests
from core.config import settings

def get_headers():
    return {"Authorization": f"Bearer {settings.BACKEND_API_KEY}"}

def get_claim(claim_id):
    url = f"{settings.BACKEND_URL}/claims/{claim_id}"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def update_claim(claim_id, data):
    url = f"{settings.BACKEND_URL}/claims/{claim_id}"
    resp = requests.put(url, json=data, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_pending_claims():
    url = f"{settings.BACKEND_URL}/claims?status=Pending"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_provider(provider_id):
    url = f"{settings.BACKEND_URL}/providers/{provider_id}"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_risk(risk_id):
    url = f"{settings.BACKEND_URL}/risks/{risk_id}"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_patient(patient_id):
    """Get patient information"""
    url = f"{settings.BACKEND_URL}/patients/{patient_id}"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_insurance_policy(policy_id):
    """Get insurance policy information"""
    url = f"{settings.BACKEND_URL}/policies/{policy_id}"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_claim_riders(claim_id):
    """Get claim riders associated with a claim"""
    url = f"{settings.BACKEND_URL}/claims/{claim_id}/riders"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()