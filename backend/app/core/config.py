from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Crypto Advisor API"
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"


settings = Settings()
