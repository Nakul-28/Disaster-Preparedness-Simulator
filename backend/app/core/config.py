from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Disaster Preparedness Simulator"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # MongoDB
    MONGODB_URL: str = "mongodb://admin:disaster2024@localhost:27017"
    MONGODB_DB_NAME: str = "disaster_prep"
    
    # ML Engine
    ML_ENGINE_URL: str = "http://localhost:8001"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
