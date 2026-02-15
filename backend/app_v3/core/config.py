import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Esoteric Knowledge Engine V3"
    VERSION: str = "3.0.0"
    API_V3_STR: str = "/api/v3"
    
    # .../backend/app_v3/core/config.py -> Go up 4 levels to root
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    DB_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'library_v3.db')}"
    
    # Feature Flags
    ENABLE_MINING_LOG: bool = True
    StrictMode: bool = True

    class Config:
        case_sensitive = True

settings = Settings()
