from core.config import settings
from openai import OpenAI
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Configure OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

REASON_CODES = {
    "AUTO_APPR": "Automatically approved - low risk routine treatment",
    "HIGH_RISK_PROVIDER": "Provider flagged for unusual claim patterns",
    "AMOUNT_EXCEEDED": "Claim amount exceeds typical range for procedure",
    "FRAUD_SUSPECTED": "Multiple claims detected, potential fraud",
    "MANUAL_REVIEW": "Requires manual review due to medium risk factors",
    "DOC_REQUIRED": "Additional documentation required",
    "POLICY_VIOLATION": "Claim violates policy terms or coverage limits",
    "PATIENT_ELIGIBILITY": "Patient eligibility issues detected",
    "COVERAGE_EXPIRED": "Policy coverage has expired",
    "PRE_AUTH_REQUIRED": "Pre-authorization required for this treatment",
    "DUPLICATE_CLAIM": "Potential duplicate claim detected",
    "AGE_RESTRICTION": "Age-related coverage restrictions from policy data apply",
    "RIDER_VIOLATION": "Claim requires riders that are not active or exceeds rider limits"
}

def assess_comprehensive_risk_with_llm(comprehensive_data) -> dict:
    """
    Use LLM to assess claim risk with comprehensive data analysis
    comprehensive_data contains: claim, provider, risk, patient, policy, riders
    Returns: dict with 'decision', 'reason_code', 'reason_description', and 'confidence_score'
    """
    try:
        claim = comprehensive_data["claim"]
        provider = comprehensive_data["provider"]
        risk = comprehensive_data["risk"]
        patient = comprehensive_data.get("patient")
        policy = comprehensive_data.get("policy")
        riders = comprehensive_data.get("riders", [])
        
        # Print comprehensive claim details to terminal
        print("=" * 80)
        print("📋 COMPREHENSIVE CLAIM ANALYSIS - ENHANCED WITH NEW DATA:")
        print("=" * 80)
        print("CLAIM INFORMATION:")
        print(json.dumps(claim, indent=2))
        print("\nPROVIDER INFORMATION:")
        print(json.dumps(provider, indent=2))
        print("\nRISK ASSESSMENT DATA:")
        print(json.dumps(risk, indent=2))
        
        if patient:
            print("\n👤 PATIENT INFORMATION:")
            print(json.dumps(patient, indent=2))
        else:
            print("\n👤 PATIENT INFORMATION: Not available")
            
        if policy:
            print("\n📄 INSURANCE POLICY INFORMATION:")
            print(json.dumps(policy, indent=2))
        else:
            print("\n📄 INSURANCE POLICY INFORMATION: Not available")
            
        if riders:
            print("\n🎯 CLAIM RIDERS:")
            print(json.dumps(riders, indent=2))
            print("\n📋 RIDER ANALYSIS:")
            active_riders = [r for r in riders if r.get('selected_status', False)]
            print(f"   Total Riders Available: {len(riders)}")
            print(f"   Active/Selected Riders: {len(active_riders)}")
            for rider in active_riders:
                print(f"   • {rider.get('name', 'Unknown')}: {rider.get('description', 'No description')}")
        else:
            print("\n🎯 CLAIM RIDERS: None")
        
        print("\n🔍 ENHANCED ANALYSIS FACTORS:")
        print(f"   Claim Status: {claim.get('status', 'N/A')}")
        print(f"   Ex Gratia Flag: {claim.get('ex_gratia_flag', 'N/A')}")
        print(f"   Appeal Case Flag: {claim.get('appeal_case_flag', 'N/A')}")
        print(f"   Submission Date: {claim.get('submission_date', 'N/A')}")
        print(f"   Last Status Update: {claim.get('last_status_update_date', 'N/A')}")
        
        if patient:
            print(f"   Patient Age Context: DOB {patient.get('date_of_birth', 'N/A')}")
            print(f"   Patient Gender: {patient.get('gender', 'N/A')}")
            print(f"   Relationship to Policy Holder: {patient.get('relationship_to_policy_holder', 'N/A')}")
            
        if policy:
            print(f"   Policy Type: {policy.get('policy_type', 'N/A')}")
            print(f"   Coverage Amount: {policy.get('coverage_amount', 'N/A')}")
            print(f"   Deductible: {policy.get('deductible_amount', 'N/A')}")
            print(f"   Copay Percentage: {policy.get('copay_percentage', 'N/A')}")
            print(f"   Policy Status: {policy.get('status', 'N/A')}")
            print(f"   Policy Start Date: {policy.get('start_date', 'N/A')}")
            print(f"   Policy End Date: {policy.get('end_date', 'N/A')}")
            
        if riders:
            active_riders = [r for r in riders if r.get('selected_status', False)]
            print(f"   Active Riders: {[r.get('name') for r in active_riders]}")
            
        print("=" * 80)
        
        
        # Prepare the comprehensive prompt for LLM
        prompt = f"""
You are an expert insurance claims analyst with access to comprehensive claim data. Analyze the following insurance claim using ALL available information and provide a detailed decision.

CLAIM INFORMATION:
{json.dumps(claim, indent=2)}

PROVIDER INFORMATION:
{json.dumps(provider, indent=2)}

RISK ASSESSMENT DATA (from backend system):
{json.dumps(risk, indent=2)}

PATIENT INFORMATION:
{json.dumps(patient, indent=2) if patient else "Not available"}

INSURANCE POLICY INFORMATION:
{json.dumps(policy, indent=2) if policy else "Not available"}

CLAIM RIDERS/ADDITIONAL COVERAGE:
{json.dumps(riders, indent=2) if riders else "None"}

BUSINESS RULES:
- Auto-approve threshold: {settings.AUTO_APPROVE_THRESHOLD}
- Auto-deny threshold: {settings.AUTO_DENY_THRESHOLD}
- Auto-approve amount limit: ${settings.AUTO_APPROVE_AMOUNT}
- Risk levels: Low (<{settings.RISK_LOW}), Medium ({settings.RISK_LOW}-{settings.RISK_MEDIUM}), High (>{settings.RISK_MEDIUM})

COMPREHENSIVE ANALYSIS INSTRUCTIONS:
You must perform a MULTI-LAYERED risk analysis considering ALL available data:

1. **CLAIM DETAILS ANALYSIS**:
   - Review claim summary for medical necessity and appropriateness
   - Check submission and update dates for timing patterns
   - Analyze ex_gratia_flag and appeal_case_flag for special considerations
   - Evaluate claim status progression

2. **PROVIDER RISK ASSESSMENT**:
   - ONLY use the risk_level field from the provider data (Low/Medium/High)
   - DO NOT make subjective judgments about provider names or locations
   - Trust the backend risk assessment system completely
   - If risk_level = "High", then consider HIGH_RISK_PROVIDER
   - If risk_level = "Low" or "Medium", do NOT flag as high-risk provider

3. **PATIENT ELIGIBILITY & DEMOGRAPHICS**:
   - Verify patient's relationship to policy holder
   - Validate patient demographics match policy records
   - Check for any eligibility restrictions in the policy data
   - Analyze patient contact information for fraud indicators

4. **POLICY COVERAGE ANALYSIS**:
   - Verify policy is active (check start_date, end_date, status)
   - Ensure treatment is covered under policy_type (Individual/Family/Group)
   - Check if claim amount is within coverage_amount limits
   - Apply deductible_amount and copay_percentage calculations
   - Review coverage_description for specific inclusions/exclusions

5. **FINANCIAL VALIDATION**:
   - Compare claim amount against annual_premium for reasonableness
   - Ensure claim doesn't exceed coverage_amount
   - Calculate patient responsibility based on deductible and copay
   - Flag unusually high amounts relative to policy value

6. **RIDERS AND ADDITIONAL COVERAGE ANALYSIS**:
   - Review any claim riders for additional coverage or restrictions
   - Validate that claimed services are covered by active riders
   - Check for rider-specific terms that might affect coverage amounts
   - Detect fraudulent rider usage (claims for inactive riders)
   - Calculate enhanced coverage benefits from active riders
   - Verify rider activation dates vs claim submission dates
   - Assess rider appropriateness for the claimed treatment type

7. **ENHANCED FRAUD AND PATTERN DETECTION**:
   - Look for unusual patterns in timing, amounts, or frequency
   - Check for suspicious provider-patient combinations
   - Identify potential duplicate or inflated claims
   - Detect rider fraud (claiming benefits for inactive/expired riders)
   - Analyze rider-claim type mismatches
   - Flag suspicious rider activation patterns

ENHANCED DECISION GUIDELINES:

2. **COVERAGE_EXPIRED** - DENY if: Policy status is "Expired" or end_date is before claim submission_date
3. **RIDER_VIOLATION** - DENY if: Claim requires riders that are not active/selected, or rider coverage is exceeded
4. **AMOUNT_EXCEEDED** - DENY if: Claim amount exceeds policy coverage_amount, rider limits, or reasonable limits
5. **PATIENT_ELIGIBILITY** - DENY if: Patient not eligible, relationship issues, eligibility restrictions from policy data
6. **FRAUD_SUSPECTED** - DENY if: Multiple fraud indicators present across data sources, including rider fraud
7. **POLICY_VIOLATION** - DENY if: Policy terms violated, coverage exclusions apply
8. **AUTO APPROVE** - APPROVE if: All validations pass, low risk, policy active, coverage sufficient, riders properly applied
9. **MANUAL_REVIEW** - PENDING if: Medium risk, conflicting assessments, complex rider scenarios
10. **DOC_REQUIRED** - PENDING if: Missing information, unclear medical necessity, rider documentation needed
11. **PRE_AUTH_REQUIRED** - PENDING if: High-cost treatment requiring authorization, especially for specialized riders

CRITICAL: Only use HIGH_RISK_PROVIDER when the backend system explicitly sets provider risk_level = "High". Do not make subjective judgments about provider names or locations - trust the data provided.

CRITICAL: Only use AGE_RESTRICTION when the policy data explicitly contains age-related restrictions. Do not make subjective judgments about what treatments are "age-appropriate" - only use restrictions that are documented in the policy or rider data.

PRIORITY ORDER: Check in this exact order and use the FIRST condition that applies:
1. HIGH_RISK_PROVIDER (immediate security concern)
2. COVERAGE_EXPIRED (fundamental eligibility)  
3. PATIENT_ELIGIBILITY (fundamental eligibility)
4. AMOUNT_EXCEEDED (financial limits)
5. FRAUD_SUSPECTED (security concern)
6. Then proceed to approval/pending decisions

Please analyze this comprehensive claim data and respond with a JSON object containing:
{{
    "decision": "Approved|Denied|Pending",
    "reason_code": "AUTO_APPR|HIGH_RISK_PROVIDER|AMOUNT_EXCEEDED|FRAUD_SUSPECTED|MANUAL_REVIEW|DOC_REQUIRED|POLICY_VIOLATION|PATIENT_ELIGIBILITY|COVERAGE_EXPIRED|PRE_AUTH_REQUIRED|DUPLICATE_CLAIM|AGE_RESTRICTION|RIDER_VIOLATION",
    "reason_description": "Detailed explanation for the decision including specific risk factors and reasoning",
    "confidence_score": 0.0-1.0,
    "risk_factors": ["list of specific risk factors identified"],
    "policy_analysis": "Analysis of policy coverage, limits, and eligibility",
    "patient_analysis": "Analysis of patient eligibility and demographics", 
    "financial_analysis": "Analysis of claim amount vs policy coverage and limits",
    "medical_necessity": "Assessment of medical necessity based on claim summary",
    "fraud_indicators": "Any fraud indicators detected across all data sources",
    "coverage_calculation": "Breakdown of coverage amounts, deductibles, and patient responsibility",
    "rider_analysis": "Detailed analysis of claim riders - active/inactive status, coverage enhancement, fraud detection",
    "rider_coverage_impact": "How riders affect coverage limits, deductibles, and approval decision",
    "analysis": "Comprehensive analysis explaining how all data sources influenced the final decision"
}}

Consider these enhanced factors in your analysis:
- **CRITICAL**: Only use provider risk_level field for provider risk decisions - do NOT analyze names/locations subjectively
- Policy status and date validity (active/expired/suspended)
- Coverage limits and claim amount validation
- Patient eligibility and relationship verification
- Age and gender appropriateness of treatments
- Deductible and copay calculations
- Medical necessity based on comprehensive patient data
- Provider risk based ONLY on the provided risk_level field (Low/Medium/High)
- Fraud detection across multiple data points (excluding subjective provider name analysis)
- Rider-specific coverage terms
- Appeal and ex-gratia considerations
- This is very important: Use real life data patterns when taking age into consideration.

IMPORTANT: Base your decision ONLY on the structured data provided. Do not make assumptions about provider quality based on names like "Dr. Sketchy" or locations like "Budget Clinic" - these may be test data. Use ONLY the risk_level field for provider risk assessment."""

        print("🤖 SENDING COMPREHENSIVE DATA TO LLM...")
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert insurance claims analyst with access to comprehensive claim data. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1500  # Increased for comprehensive analysis
        )
        
        # Parse the response
        llm_response = response.choices[0].message.content.strip()
        
        print("🤖 COMPREHENSIVE LLM RESPONSE RECEIVED:")
        print(llm_response)
        print("=" * 80)
        
        # Try to extract JSON from the response
        if llm_response.startswith("```json"):
            llm_response = llm_response[7:-3]
        elif llm_response.startswith("```"):
            llm_response = llm_response[3:-3]
            
        result = json.loads(llm_response)
        
        # Validate the response structure
        required_fields = ["decision", "reason_code", "reason_description", "confidence_score"]
        optional_fields = ["policy_analysis", "patient_analysis", "financial_analysis", 
                          "medical_necessity", "fraud_indicators", "coverage_calculation", 
                          "analysis", "risk_factors"]
        
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")
        
        # Log if optional analysis fields are missing
        for field in optional_fields:
            if field not in result:
                logger.warning(f"LLM response missing optional field: {field}")
        
        # Ensure reason_description uses our standard codes if available
        if result["reason_code"] in REASON_CODES:
            result["reason_description"] = REASON_CODES[result["reason_code"]]
        
        print("✅ COMPREHENSIVE FINAL DECISION:")
        print(f"   Decision: {result['decision']}")
        print(f"   Reason: {result['reason_code']}")
        print(f"   Confidence: {result['confidence_score']}")
        print(f"   Policy Analysis: {result.get('policy_analysis', 'N/A')[:100]}...")
        print(f"   Patient Analysis: {result.get('patient_analysis', 'N/A')[:100]}...")
        print(f"   Financial Analysis: {result.get('financial_analysis', 'N/A')[:100]}...")
        print(f"   Medical Necessity: {result.get('medical_necessity', 'N/A')[:100]}...")
        print(f"   Fraud Indicators: {result.get('fraud_indicators', 'N/A')}")
        print("=" * 80)
        
        logger.info(f"Comprehensive LLM assessment completed for claim. Decision: {result['decision']}, Confidence: {result['confidence_score']}")
        return result
        
    except Exception as e:
        print(f"❌ COMPREHENSIVE LLM ASSESSMENT FAILED: {str(e)}")
        print("=" * 80)
        logger.error(f"Comprehensive LLM assessment failed: {str(e)}. Returning error response.")
        return {
            "decision": "Pending",
            "reason_code": "AI_ERROR",
            "reason_description": f"AI assessment failed: {str(e)}. Manual review required.",
            "confidence_score": 0.0
        }

def assess_risk_with_llm(claim, provider, risk) -> dict:
    """
    Backwards compatibility wrapper for the original function signature
    """
    comprehensive_data = {
        "claim": claim,
        "provider": provider,
        "risk": risk,
        "patient": None,
        "policy": None,
        "riders": []
    }
    return assess_comprehensive_risk_with_llm(comprehensive_data)

# Main functions
def assess_risk(claim, provider, risk) -> float:
    """Main assessment function using LLM - backwards compatibility"""
    result = assess_risk_with_llm(claim, provider, risk)
    return result["confidence_score"]

def decide_claim(score, claim, provider, risk):
    """Main decision function using LLM - backwards compatibility"""
    result = assess_risk_with_llm(claim, provider, risk)
    return result["decision"], result["reason_code"], result["reason_description"]

def process_claim_with_ai(data_input, provider=None, risk=None):
    """
    Main function to process a claim using AI
    Can handle both old format (claim, provider, risk) and new comprehensive format
    Returns complete assessment with decision, reasoning, and confidence
    """
    if isinstance(data_input, dict) and "claim" in data_input:
        # New comprehensive format
        return assess_comprehensive_risk_with_llm(data_input)
    else:
        # Old format - backwards compatibility
        return assess_risk_with_llm(data_input, provider, risk)