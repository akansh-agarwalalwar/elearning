from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False

class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")

@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig}
    return configs[env_state]()

config = get_config(BaseConfig().ENV_STATE)

DATABASE_URL = config.DATABASE_URL