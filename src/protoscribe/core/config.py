from pydantic_settings import BaseSettings
from typing import List, Dict, Any
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    PROJECT_NAME: str = "ProtoScribe"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./protoscribe.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM APIs
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "openai"
    DEFAULT_MODEL: str = "gpt-4"
    
    # LLM Configuration
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2000
    LLM_TIMEOUT: int = 30
    
    # AI Analysis Settings
    MIN_CONFIDENCE_THRESHOLD: float = 0.6
    MAX_SUGGESTIONS_PER_ITEM: int = 3
    ENABLE_ADVANCED_ANALYSIS: bool = True
    
    # File Processing
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".txt"]
    UPLOAD_DIR: str = "uploads"
    
    # Compliance Guidelines
    GUIDELINES_DIR: str = "guidelines"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
