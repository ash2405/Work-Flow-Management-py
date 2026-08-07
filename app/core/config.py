from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
class Settings(BaseSettings):
    # Application
    APP_NAME : str
    APP_VERSION : str
    DEBUG : bool

    # Server
    HOST : str
    PORT : int

    # Database
    DATABASE_URL : str

    #JWT
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    # Redies
    REDIS_URL : str

    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        case_sensitive = True,
        extra = 'ignore'
    )

# Without @lru_cache, a new Settings object is created
# every time Settings() is called.
@lru_cache
def get_settings()-> Settings:
    return Settings()


settings = get_settings()