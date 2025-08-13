# Insurance Claim AI Processing Service

A standalone AI-powered microservice for automated insurance claim processing with **LLM (Large Language Model) integration**.

## Core Features

- **🤖 AI-Powered Assessment**: Choose between LLM-based intelligent analysis or traditional rule-based processing
- **🎯 Risk Assessment**: Provider history, claim amount, frequency, and treatment analysis
- **⚡ Automated Decision Making**: Approve, deny, or flag claims based on AI-driven risk scores
- **📊 Batch Processing**: Automatically process all pending claims
- **🔗 REST API**: Integrate easily with your backend
- **🔄 Flexible Processing**: Seamless fallback from LLM to rule-based when needed

## AI Assessment Methods

### 1. LLM-Based Assessment (Recommended)
Uses OpenAI's GPT models to analyze claims with human-like reasoning:
- **Intelligent Analysis**: Contextual understanding of medical procedures and risks
- **Detailed Reasoning**: Provides explanations for each decision
- **Risk Factor Identification**: Automatically identifies specific risk indicators
- **Adaptive Learning**: Improves with different claim types and scenarios

### 2. Rule-Based Assessment (Fallback)
Traditional algorithmic approach using predefined rules:
- **Fast Processing**: Immediate decisions based on thresholds
- **Predictable Results**: Consistent rule-based outcomes
- **Reliable Fallback**: Ensures service continuity if LLM is unavailable

## Configuration

### LLM Setup
```bash
# Enable LLM-based assessment
USE_LLM=true
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4, gpt-4-turbo-preview

# Disable LLM (use rule-based only)
USE_LLM=false
```

### Risk Thresholds
```bash
RISK_LOW=0.3
RISK_MEDIUM=0.7
AUTO_APPROVE_THRESHOLD=0.3
AUTO_DENY_THRESHOLD=0.8
AUTO_APPROVE_AMOUNT=5000
```

## API Endpoints

- `POST /api/v1/claims/process` — Process a single claim by ID (uses AI assessment)
- `POST /api/v1/claims/process-pending` — Process all pending claims (uses AI assessment)
- `GET /health` — Health and connectivity check

## Response Format

When LLM is enabled, responses include additional AI analysis:

```json
{
  "status": "Approved|Denied|Pending",
  "reason_code": "AUTO_APPR|HIGH_RISK_PROVIDER|FRAUD_SUSPECTED|...",
  "reason_description": "Detailed explanation",
  "confidence_score": 0.85,
  "ai_analysis": "AI's reasoning for the decision",
  "risk_factors": ["factor1", "factor2"]
}
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and preferences
   ```

3. **Test the LLM integration:**
   ```bash
   python test_llm.py
   ```

4. **Run the service:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access API docs:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Security

- All endpoints require API key authentication (header: `api-key`)
- OpenAI API key is securely managed through environment variables
- Audit logging and input validation included

## Customization

### AI Service (`services/ai_service.py`)
- **LLM Prompts**: Customize the AI prompts for different assessment criteria
- **Risk Thresholds**: Adjust automatic approval/denial thresholds
- **Fallback Logic**: Modify rule-based assessment for specific scenarios

### Assessment Methods
- **`process_claim_with_ai()`**: Main AI assessment function (recommended)
- **`assess_risk()`**: Backward compatible function for existing integrations
- **`decide_claim()`**: Backward compatible decision function

## Project Structure

```
jay-claimsub-ai/
├── main.py                    # FastAPI application entry point
├── models.py                  # Database models
├── schemas.py                 # Pydantic schemas
├── database.py               # Database configuration
├── requirements.txt          # Dependencies (now includes openai)
├── test_llm.py              # LLM integration test script
├── .env.example             # Environment configuration template
├── services/
│   ├── ai_service.py        # 🤖 AI assessment logic (LLM + rule-based)
│   ├── claim_processor.py   # Claim processing workflow
│   └── backend_client.py    # Backend API client
├── api/
│   └── v1/
│       └── endpoints/
│           └── claims.py    # REST API endpoints
└── core/
    ├── config.py           # Configuration with LLM settings
    └── security.py        # API security
```
