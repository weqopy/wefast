from pydantic import BaseSettings
from pathlib import Path

DATA_DIR = Path.cwd()


class Settings(BaseSettings):
    PRODUCTION: bool = False


settings = Settings()
