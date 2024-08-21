# config/settings.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mariadb_user: str = "your_mariadb_user"
    mariadb_password: str = "your_mariadb_password"
    mariadb_db: str = "your_mariadb_db"
    mariadb_host: str = "your_mariadb_host"
    mariadb_port: int = 3306

    redis_host: str = "your_redis_host"
    redis_port: int = 6379
    redis_ttl: int = 3600  # 1시간

    openai_api_key: str = "your_openai_api_key"

    class Config:
        env_file = ".env"


settings = Settings()
