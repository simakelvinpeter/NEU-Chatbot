from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    from pydantic import Field

    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "NEU Virtual Assistant API"
    DEBUG: bool = True

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
