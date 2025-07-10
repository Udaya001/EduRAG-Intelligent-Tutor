from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):

    # Network settings
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)  # empty list by default
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])  # default allow all

    # API keys and database credentials
    GOOGLE_API_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str

    # Other settings
    VECTOR_STORE_TYPE: str = "chroma"
    LOG_LEVEL: str = "INFO"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"


# Initialize settings
settings = Settings()
