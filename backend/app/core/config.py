from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_ENDPOINT: str
    LLM_API_KEY: str
    LLM_MODEL: str
    FERNET_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    DATABASE_PATH: str
    LOG_STORAGE_PATH: str
    REPORT_STORAGE_PATH: str
    CODE_INDEX_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()
