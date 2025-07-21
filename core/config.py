import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./insurance.db")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "changeme")
    RISK_LOW: float = float(os.getenv("RISK_LOW", 0.3))
    RISK_MEDIUM: float = float(os.getenv("RISK_MEDIUM", 0.7))
    RISK_HIGH: float = float(os.getenv("RISK_HIGH", 1.0))
    AUTO_APPROVE_THRESHOLD: float = float(os.getenv("AUTO_APPROVE_THRESHOLD", 0.3))
    AUTO_DENY_THRESHOLD: float = float(os.getenv("AUTO_DENY_THRESHOLD", 0.8))
    AUTO_APPROVE_AMOUNT: float = float(os.getenv("AUTO_APPROVE_AMOUNT", 5000))

settings = Settings()