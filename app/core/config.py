import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    allow_origins: str
    log_to_file: bool
    log_level: str

    class Config:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        env_file = os.path.join(project_root, '.env')

settings = Settings()
