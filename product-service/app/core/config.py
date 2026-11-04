from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
from typing import Literal


class Settings(BaseSettings):


    app_name: str = "ProductService"
    debug: bool = False
    environment: Literal['development', 'staging', 'production'] = 'development'

    # Srv settings
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # DB settings
    database_url: PostgresDsn
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_echo: bool = False 

    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    redis_max_connections: int = 10
    redis_enabled: bool = True

    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    secret_key: str
    access_token_expires_in: int = 3600  # seconds

    # Cache TTLs (seconds)
    cache_ttl_products: int = 300
    cache_ttl_product_detail: int = 600

    allowed_origins: list[str] = ["*"]

    @field_validator('database_url')
    def validate_db_url(cls, v):
        if not str(v).startswith(('postgresql://', 'postgresql+psycopg2://')):
            raise ValueError('database_url debe ser una URL de PostgreSQL válida')
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False 


def get_settings() -> Settings:
    """
    Returns cached settings instance.
    Using lru_cache ensures settings are loaded once.
    """
    return Settings()