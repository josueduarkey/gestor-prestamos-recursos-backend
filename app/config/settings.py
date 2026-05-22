from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MAILTRAP_HOST: str = "smtp.mailtrap.io"
    MAILTRAP_PORT: int = 587
    MAILTRAP_USER: str = ""
    MAILTRAP_PASSWORD: str = ""
    MAIL_FROM: str = "no-reply@keytest.edu.sv"
    MAIL_FROM_NAME: str = "Key Institute"
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_database_url(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
