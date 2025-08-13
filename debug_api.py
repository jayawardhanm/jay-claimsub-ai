#!/usr/bin/env python3
"""
Comprehensive API test script showing correct usage
"""

import requests
import json
import os

API_BASE_URL = "http://127.0.0.1:8080"

def test_correct_request():
    """Show the correct way to make a request"""
    print("✅ CORRECT REQUEST:")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": "changeme"  # This matches BACKEND_API_KEY in .env
    }
    
    payload = {
        "claim_id": "CLM-DEMO-001"
    }
    
    print(f"URL: {API_BASE_URL}/api/v1/claims/process")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/claims/process",
        headers=headers,
        json=payload
    )
    
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Response:")
        print(json.dumps(result, indent=2))
        return True
    else:
        print(f"❌ FAILED: {response.text}")
        return False

def test_missing_api_key():
    """Show what happens without api-key header"""
    print("\n❌ MISSING API KEY:")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json"
        # Missing api-key header
    }
    
    payload = {
        "claim_id": "CLM-DEMO-001"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/claims/process",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Error: {response.text}")

def test_wrong_api_key():
    """Show what happens with wrong api-key"""
    print("\n❌ WRONG API KEY:")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": "wrong-key"
    }
    
    payload = {
        "claim_id": "CLM-DEMO-001"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/claims/process",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Error: {response.text}")

def test_missing_claim_id():
    """Show what happens without claim_id in payload"""
    print("\n❌ MISSING CLAIM_ID:")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": "changeme"
    }
    
    payload = {
        "wrong_field": "some_value"
        # Missing claim_id field
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/claims/process",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Error: {response.text}")

def test_malformed_json():
    """Show what happens with malformed JSON"""
    print("\n❌ MALFORMED JSON:")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": "changeme"
    }
    
    # Sending malformed JSON as string instead of using json parameter
    malformed_data = '{"claim_id": "test"'  # Missing closing brace
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/claims/process",
        headers=headers,
        data=malformed_data  # Using data instead of json
    )
    
    print(f"Status: {response.status_code}")
    print(f"Error: {response.text}")

def test_llm_vs_rule_based():
    """Test both LLM and rule-based assessment"""
    print("\n🤖 TESTING LLM vs RULE-BASED:")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": "changeme"
    }
    
    # Test with LLM (current setting)
    payload = {"claim_id": "CLM-LLM-TEST"}
    response = requests.post(f"{API_BASE_URL}/api/v1/claims/process", headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("🤖 LLM Assessment Result:")
        print(f"   Decision: {result.get('status')}")
        print(f"   Reason: {result.get('reason_description')}")
        print(f"   Confidence: {result.get('confidence_score')}")
        if 'ai_analysis' in result:
            print(f"   AI Analysis: {result['ai_analysis']}")
    else:
        print(f"❌ LLM test failed: {response.text}")

def main():
    print("🚀 Insurance Claims API - Test Suite")
    print("🔧 Configuration:")
    print(f"   Server: {API_BASE_URL}")
    print(f"   API Key: changeme (from .env file)")
    print(f"   LLM Enabled: true")
    print(f"   Mock Data: true")
    print()
    
    # Test server health first
    try:
        health = requests.get(f"{API_BASE_URL}/health")
        if health.status_code != 200:
            print("❌ Server is not running! Please start it first:")
            print("   python main.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server! Please start it first:")
        print("   python main.py")
        return
    
    # Run all tests
    success = test_correct_request()
    test_missing_api_key()
    test_wrong_api_key()
    test_missing_claim_id()
    test_malformed_json()
    
    if success:
        test_llm_vs_rule_based()
    
    print("\n" + "=" * 60)
    print("📝 SUMMARY - Common 422 Error Causes:")
    print("1. Missing 'api-key' header")
    print("2. Wrong API key (must match BACKEND_API_KEY in .env)")
    print("3. Missing 'claim_id' field in JSON payload")
    print("4. Malformed JSON in request body")
    print("5. Wrong Content-Type header")
    print()
    print("✅ Correct request format:")
    print("   Headers: {'Content-Type': 'application/json', 'api-key': 'changeme'}")
    print("   Body: {'claim_id': 'your-claim-id'}")

if __name__ == "__main__":
    main()
