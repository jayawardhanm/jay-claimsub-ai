# Insurance Claim AI Processing Service

A standalone AI-powered microservice for automated insurance claim processing.

## Core Features

- **Risk Assessment**: Provider history, claim amount, frequency, and treatment analysis
- **Automated Decision Making**: Approve, deny, or flag claims based on AI-driven risk scores
- **Batch Processing**: Automatically process all pending claims
- **REST API**: Integrate easily with your backend

## API Endpoints

- `POST /api/v1/claims/process` — Process a single claim by ID
- `POST /api/v1/claims/process-pending` — Process all pending claims
- `GET /health` — Health and connectivity check

## Project Structure

```
insurance-ai-service/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── services/
│   │   ├── ai_service.py
│   │   └── claim_processor.py
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── claims.py
│   └── core/
│       ├── config.py
│       └── security.py
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Quickstart

1. **Clone the repo & set up your `.env` file**  
2. **Run locally with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
3. **Access API docs:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Security

- All endpoints require API key authentication (header: `api-key`)
- Audit logging and input validation included

## Customize

- Adjust risk thresholds and behavior in `.env`
- Extend AI logic in `app/services/ai_service.py`
