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
    "DOC_REQUIRED": "Additional documentation required"
}

def assess_risk_with_llm(claim, provider, risk) -> dict:
    """
    Use LLM to assess claim risk and make decision
    Returns: dict with 'decision', 'reason_code', 'reason_description', and 'confidence_score'
    """
    try:
        # Print claim details to terminal
        print("=" * 60)
        print("📋 CLAIM DETAILS BEING SENT TO LLM:")
        print("=" * 60)
        print("CLAIM INFORMATION:")
        print(json.dumps(claim, indent=2))
        print("\nPROVIDER INFORMATION:")
        print(json.dumps(provider, indent=2))
        print("\nRISK ASSESSMENT DATA:")
        print(json.dumps(risk, indent=2))
        print("\n🎯 KEY FIELDS FOR ANALYSIS:")
        print(f"   Claim ID: {claim.get('id', 'N/A')}")
        print(f"   Claim Amount: ${claim.get('amount', 'N/A')}")
        print(f"   Claim Summary: {claim.get('summary', 'N/A')}")
        print(f"   Provider Risk Level: {provider.get('risk_level', 'N/A')}")
        print(f"   Provider Name: {provider.get('name', 'N/A')}")
        print(f"   Backend Risk ID: {risk.get('risk_id', 'N/A')}")
        print(f"   Backend Risk Level: {risk.get('risk_level', 'N/A')}")
        print(f"   Backend Risk Score: {risk.get('score', 'N/A')}")
        print(f"   Backend Risk Description: {risk.get('description', 'N/A')}")
        print("\n🔍 DUAL ANALYSIS MODE:")
        print("   1. Backend Risk Assessment Review")
        print("   2. Independent Claim Summary Analysis")
        print("=" * 60)
        
        # Prepare the prompt for LLM
        prompt = f"""
You are an expert insurance claims analyst. Analyze the following insurance claim and provide a decision.

CLAIM INFORMATION:
{json.dumps(claim, indent=2)}

PROVIDER INFORMATION:
{json.dumps(provider, indent=2)}

RISK ASSESSMENT DATA (from backend system):
{json.dumps(risk, indent=2)}

BUSINESS RULES:
- Auto-approve threshold: {settings.AUTO_APPROVE_THRESHOLD}
- Auto-deny threshold: {settings.AUTO_DENY_THRESHOLD}
- Auto-approve amount limit: ${settings.AUTO_APPROVE_AMOUNT}
- Risk levels: Low (<{settings.RISK_LOW}), Medium ({settings.RISK_LOW}-{settings.RISK_MEDIUM}), High (>{settings.RISK_MEDIUM})

ANALYSIS INSTRUCTIONS:
You must perform TWO types of risk analysis and combine them:

1. **BACKEND RISK ASSESSMENT REVIEW**: 
   - Review the pre-calculated risk data from the backend system (risk_id: {risk.get('risk_id', 'N/A')})
   - Consider the existing risk_level and risk_description
   - Validate if this assessment seems appropriate

2. **INDEPENDENT CLAIM SUMMARY ANALYSIS**:
   - Analyze the claim summary directly from the claim information
   - Make your own medical necessity judgment based on the treatment described
   - Assess if the procedure/treatment seems reasonable for the condition
   - Identify any red flags in the claim description itself
   - Consider claim amount vs. typical costs for this type of treatment

3. **COMBINED DECISION**:
   - Compare your independent analysis with the backend risk assessment
   - If they align: proceed with confidence
   - If they conflict: explain the discrepancy and lean toward the more conservative assessment
   - Factor in provider history and location risks

DECISION GUIDELINES:
1. If overall risk is LOW (both assessments) and no red flags: "Approved" with reason_code "AUTO_APPR"
2. If provider has high risk patterns or location issues: "Denied" with reason_code "HIGH_RISK_PROVIDER"
3. If fraud indicators present (either assessment): "Denied" with reason_code "FRAUD_SUSPECTED"
4. If medium risk or assessments conflict: "Pending" with reason_code "MANUAL_REVIEW"
5. If documentation missing or claim summary unclear: "Pending" with reason_code "DOC_REQUIRED"
6. If claim amount exceeds reasonable limits: "Denied" with reason_code "AMOUNT_EXCEEDED"

Please analyze this claim and respond with a JSON object containing:
{{
    "decision": "Approved|Denied|Pending",
    "reason_code": "AUTO_APPR|HIGH_RISK_PROVIDER|AMOUNT_EXCEEDED|FRAUD_SUSPECTED|MANUAL_REVIEW|DOC_REQUIRED",
    "reason_description": "Detailed explanation for the decision including specific risk factors and reasoning",
    "confidence_score": 0.0-1.0,
    "risk_factors": ["list of specific risk factors identified"],
    "backend_risk_assessment": "Your evaluation of the pre-calculated risk data",
    "claim_summary_analysis": "Your independent analysis of the claim summary and medical necessity",
    "analysis": "Combined analysis explaining how both assessments influenced your final decision"
}}

Consider these factors in your analysis:
- Medical necessity based on claim summary (independent analysis)
- Backend risk assessment validation
- Provider's historical performance and risk level
- Location-based risk factors
- Presence of fraud indicators
- Claim complexity and documentation quality
- Claim amount reasonableness

Base your decision on the actual data provided, not assumptions. Always explain how both the backend risk assessment and your independent claim analysis contributed to your decision."""

        print("🤖 SENDING TO LLM...")
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert insurance claims analyst. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        # Parse the response
        llm_response = response.choices[0].message.content.strip()
        
        print("🤖 LLM RESPONSE RECEIVED:")
        print(llm_response)
        print("=" * 60)
        
        # Try to extract JSON from the response
        if llm_response.startswith("```json"):
            llm_response = llm_response[7:-3]
        elif llm_response.startswith("```"):
            llm_response = llm_response[3:-3]
            
        result = json.loads(llm_response)
        
        # Validate the response structure
        required_fields = ["decision", "reason_code", "reason_description", "confidence_score"]
        optional_fields = ["backend_risk_assessment", "claim_summary_analysis", "analysis", "risk_factors"]
        
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
        
        print("✅ FINAL DECISION:")
        print(f"   Decision: {result['decision']}")
        print(f"   Reason: {result['reason_code']}")
        print(f"   Confidence: {result['confidence_score']}")
        print(f"   Backend Risk Assessment: {result.get('backend_risk_assessment', 'N/A')}")
        print(f"   Claim Summary Analysis: {result.get('claim_summary_analysis', 'N/A')}")
        print(f"   Combined Analysis: {result.get('analysis', 'N/A')}")
        print("=" * 60)
        
        logger.info(f"LLM assessment completed for claim. Decision: {result['decision']}, Confidence: {result['confidence_score']}")
        return result
        
    except Exception as e:
        print(f"❌ LLM ASSESSMENT FAILED: {str(e)}")
        print("=" * 60)
        logger.error(f"LLM assessment failed: {str(e)}. Returning error response.")
        return {
            "decision": "Pending",
            "reason_code": "AI_ERROR",
            "reason_description": f"AI assessment failed: {str(e)}. Manual review required.",
            "confidence_score": 0.0
        }

# Main functions
def assess_risk(claim, provider, risk) -> float:
    """Main assessment function using LLM"""
    result = assess_risk_with_llm(claim, provider, risk)
    return result["confidence_score"]

def decide_claim(score, claim, provider, risk):
    """Main decision function using LLM"""
    result = assess_risk_with_llm(claim, provider, risk)
    return result["decision"], result["reason_code"], result["reason_description"]

def process_claim_with_ai(claim, provider, risk):
    """
    Main function to process a claim using AI
    Returns complete assessment with decision, reasoning, and confidence
    """
    return assess_risk_with_llm(claim, provider, risk)