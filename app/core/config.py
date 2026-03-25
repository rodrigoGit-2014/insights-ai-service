import json
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, computed_field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="postgresql://sales_user:sales_password@localhost:5432/sales_db")
    REDIS_URL: str = Field(default="redis://localhost:6379/3")
    APP_NAME: str = Field(default="Insights AI Service")
    APP_VERSION: str = Field(default="1.0.0")
    LOG_LEVEL: str = Field(default="INFO")
    DEBUG: bool = Field(default=False)
    CORS_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:5173")

    @computed_field
    @property
    def cors_origins_list(self) -> List[str]:
        try:
            parsed = json.loads(self.CORS_ORIGINS)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    API_V1_PREFIX: str = Field(default="/api/v1")
    PORT: int = Field(default=8003)
    JWT_SECRET: str = Field(default="change-me-in-production-use-a-long-random-string")

    # LLM
    ANTHROPIC_API_KEY: str = Field(default="")
    LLM_MODEL: str = Field(default="claude-sonnet-4-20250514")
    LLM_MAX_TOKENS: int = Field(default=4096)
    LLM_TEMPERATURE: float = Field(default=0.3)

    # Service URLs
    SALES_SERVICE_URL: str = Field(default="http://localhost:8000/api/v1")
    APRIORI_SERVICE_URL: str = Field(default="http://localhost:8002/api/v1")

    # Reports
    REPORT_OUTPUT_DIR: str = Field(default="/tmp/insights_reports")
    REPORT_TTL_HOURS: int = Field(default=24)

    # Cache
    INSIGHT_CACHE_TTL_SECONDS: int = Field(default=3600)

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
