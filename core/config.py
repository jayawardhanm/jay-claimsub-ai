import os

class Settings:
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    BACKEND_API_KEY: str = os.getenv("BACKEND_API_KEY", "changeme")
    RISK_LOW: float = float(os.getenv("RISK_LOW", 0.3))
    RISK_MEDIUM: float = float(os.getenv("RISK_MEDIUM", 0.7))
    RISK_HIGH: float = float(os.getenv("RISK_HIGH", 1.0))
    AUTO_APPROVE_THRESHOLD: float = float(os.getenv("AUTO_APPROVE_THRESHOLD", 0.3))
    AUTO_DENY_THRESHOLD: float = float(os.getenv("AUTO_DENY_THRESHOLD", 0.8))
    AUTO_APPROVE_AMOUNT: float = float(os.getenv("AUTO_APPROVE_AMOUNT", 5000))
    
    # OpenAI/LLM settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "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")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    USE_LLM: bool = os.getenv("USE_LLM", "false").lower() == "true"

settings = Settings()