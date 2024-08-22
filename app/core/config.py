from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mariadb_user: str
    mariadb_password: str
    mariadb_db: str
    mariadb_host: str
    mariadb_port: int
    redis_host: str
    redis_port: int
    openai_api_key: str
    jwt_secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
