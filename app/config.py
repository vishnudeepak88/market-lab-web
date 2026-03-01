import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Market Lab Web"
    env: str = os.getenv("ENV", "development")
    port: int = int(os.getenv("PORT", "8000"))

    database_url: Optional[str] = os.getenv("DATABASE_URL")

    # In demo/dev, default to dev-key. In prod, you MUST set it explicitly.
    api_key: Optional[str] = os.getenv("MARKETLAB_API_KEY") or (
        "dev-key" if os.getenv("ENV", "development") == "development" else None
    )

    git_sha: Optional[str] = os.getenv("GIT_SHA")

    # Scoring weights
    momentum_w: float = float(os.getenv("MOMENTUM_W", "100"))
    trend_w: float = float(os.getenv("TREND_W", "60"))
    risk_w: float = float(os.getenv("RISK_W", "80"))
    liquidity_w: float = float(os.getenv("LIQUIDITY_W", "20"))

    class Config:
        env_file = ".env"


settings = Settings()
