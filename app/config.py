from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://user:pass@db:5432/test_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
