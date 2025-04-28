from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")

    APILAYER_KEY: str
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite+aiosqlite:///./complaints.db"


settings = Settings()
