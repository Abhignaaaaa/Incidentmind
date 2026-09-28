from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/incidentmind"
    HINDSIGHT_URL: str = "https://api.hindsight.vectorize.io"
    HINDSIGHT_API_KEY: str = ""
    HINDSIGHT_BANK_ID: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
