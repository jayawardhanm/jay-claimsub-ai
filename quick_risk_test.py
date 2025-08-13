#!/usr/bin/env python3
"""
Quick test to verify AI respects risk_level field and ignores suspicious names
"""

from services.ai_service import assess_comprehensive_risk_with_llm

def test_risk_level_respect():
    """Test that AI respects risk_level=Low even with suspicious names"""
    
    test_data = {
        "claim": {
            "claim_id": "CLM-TEST-001",
            "provider_id": "PROV-TEST-001",
            "risk_id": "RISK-TEST-001", 
            "policy_id": "POL-TEST-001",
            "patient_id": "PAT-TEST-001",
            "status": "Pending",
            "submission_date": "2024-07-20",
            "summary": "Routine checkup and basic medical examination.",
            "ex_gratia_flag": False,
            "appeal_case_flag": False,
            "amount": "200"  # Small amount
        },
        "provider": {
            "provider_id": "PROV-TEST-001",
            "first_name": "Dr. Suspicious",
            "last_name": "Sketchy",
            "location": "Unknown Clinic, Fraud City",
            "risk_level": "Low",  # EXPLICIT LOW RISK
            "name": "Dr. Suspicious Sketchy"
        },
        "risk": {
            "risk_id": "RISK-TEST-001",
            "name": "Low Risk Assessment",
            "description": "Low risk routine care",
            "risk_level": "Low",
            "score": 0.1
        },
        "patient": {
            "patient_id": "PAT-TEST-001",
            "policy_id": "POL-TEST-001",
            "first_name": "Test",
            "last_name": "Patient",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "phone_number": "+1-555-0000",
            "email": "test@test.com",
            "address": "123 Test Street",
            "relationship_to_policy_holder": "Self"
        },
        "policy": {
            "policy_id": "POL-TEST-001",
            "policy_number": "TEST-001",
            "policy_name": "Test Policy",
            "policy_type": "Individual",
            "coverage_amount": "50000",
            "annual_premium": "1200",
            "deductible_amount": "500",
            "copay_percentage": "20",
            "coverage_description": "Test coverage",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "status": "Active"
        },
        "riders": []
    }
    
    print("🧪 TESTING RISK_LEVEL RESPECT")
    print("=" * 60)
    print(f"Provider Name: {test_data['provider']['name']} (suspicious name)")
    print(f"Provider Location: {test_data['provider']['location']} (suspicious location)")
    print(f"Provider risk_level: {test_data['provider']['risk_level']} (EXPLICIT)")
    print("🎯 EXPECTED: Should NOT be HIGH_RISK_PROVIDER")
    print("=" * 60)
    
    result = assess_comprehensive_risk_with_llm(test_data)
    
    print(f"\n🎯 RESULT: {result.get('decision', 'N/A')}")
    print(f"📋 REASON: {result.get('reason_code', 'N/A')}")
    
    if result.get('reason_code') == 'HIGH_RISK_PROVIDER':
        print("❌ FAILED: AI ignored risk_level=Low and used name/location")
    else:
        print("✅ SUCCESS: AI respected risk_level field")
    
    return result

if __name__ == "__main__":
    test_risk_level_respect()
