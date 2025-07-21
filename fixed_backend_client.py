import httpx
import os
from sqlalchemy.inspection import inspect
import logging

logger = logging.getLogger(__name__)
AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL", "http://localhost:8080/api/v1/claims/process")
AI_SERVICE_API_KEY = os.environ.get("AI_SERVICE_API_KEY", "changeme")

def sqlalchemy_to_dict(obj):
    """Convert SQLAlchemy object to JSON-serializable dictionary"""
    result = {}
    for c in inspect(obj).mapper.column_attrs:
        value = getattr(obj, c.key)
        # Convert non-serializable types to strings
        if hasattr(value, '__str__') and not isinstance(value, (str, int, float, bool, type(None))):
            value = str(value)
        result[c.key] = value
    return result

async def process_claim_with_ai(claim_data):
    """Process claim with AI service, with fallback if service is unavailable"""
    # If it's a SQLAlchemy object, convert it first
    if hasattr(claim_data, '__tablename__'):
        claim_dict = sqlalchemy_to_dict(claim_data)
    else:
        claim_dict = claim_data
    
    # Extract claim_id for the AI service request
    claim_id = claim_dict.get('claim_id') or claim_dict.get('id')
    
    if not claim_id:
        logger.error("No claim_id found in claim data")
        return {
            "status": "Pending",
            "reason_code": "MISSING_CLAIM_ID",
            "reason_description": "Claim ID is required for AI processing. Claim requires manual review."
        }
    
    try:
        # Prepare the request in the format expected by the AI service
        ai_request_payload = {"claim_id": str(claim_id)}
        
        # Set up headers with API key authentication
        headers = {
            "Content-Type": "application/json",
            "api-key": AI_SERVICE_API_KEY
        }
        
        logger.info(f"Sending claim {claim_id} to AI service at {AI_SERVICE_URL}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                AI_SERVICE_URL, 
                json=ai_request_payload,
                headers=headers
            )
            response.raise_for_status()
            
            ai_result = response.json()
            logger.info(f"AI service processed claim {claim_id}: {ai_result.get('status')}")
            
            return ai_result
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 422:
            logger.error(f"AI service validation error for claim {claim_id}: {e.response.text}")
            return {
                "status": "Pending",
                "reason_code": "AI_VALIDATION_ERROR",
                "reason_description": f"AI service validation failed: {e.response.text}. Claim requires manual review."
            }
        elif e.response.status_code == 401:
            logger.error(f"AI service authentication failed for claim {claim_id}: Invalid API key")
            return {
                "status": "Pending",
                "reason_code": "AI_AUTH_ERROR",
                "reason_description": "AI service authentication failed. Claim requires manual review."
            }
        else:
            logger.error(f"AI service HTTP error for claim {claim_id}: {e.response.status_code} - {e.response.text}")
            return {
                "status": "Pending",
                "reason_code": "AI_HTTP_ERROR",
                "reason_description": f"AI service returned error {e.response.status_code}. Claim requires manual review."
            }
            
    except httpx.RequestError as e:
        logger.warning(f"AI service connection error for claim {claim_id}: {e}. Using fallback decision.")
        return {
            "status": "Pending",
            "reason_code": "AI_UNAVAILABLE",
            "reason_description": "AI service is currently unavailable. Claim requires manual review."
        }
    except Exception as e:
        logger.error(f"Unexpected error processing claim {claim_id} with AI: {e}")
        return {
            "status": "Pending",
            "reason_code": "AI_ERROR",
            "reason_description": "Unexpected error occurred during AI processing. Claim requires manual review."
        }

async def test_ai_service_connection():
    """Test connection to AI service"""
    try:
        health_url = AI_SERVICE_URL.replace('/api/v1/claims/process', '/health')
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(health_url)
            response.raise_for_status()
            
            health_data = response.json()
            logger.info(f"AI service health check passed: {health_data}")
            return True
            
    except Exception as e:
        logger.warning(f"AI service health check failed: {e}")
        return False

# Environment variable configuration for your backend .env file:
"""
Add these to your backend's .env file:

# AI Service Configuration
AI_SERVICE_URL=http://localhost:8080/api/v1/claims/process
AI_SERVICE_API_KEY=changeme

# Alternative if AI service is running on different host/port:
# AI_SERVICE_URL=http://ai-service-host:8080/api/v1/claims/process
"""
