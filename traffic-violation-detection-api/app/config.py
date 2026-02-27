"""
Application configuration via environment variables.
"""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    MODEL_PATH: str = os.getenv("MODEL_PATH", "")
    DEVICE: str = os.getenv("DEVICE", "cpu")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    DEFAULT_CONFIDENCE: float = float(os.getenv("DEFAULT_CONFIDENCE", "0.5"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
