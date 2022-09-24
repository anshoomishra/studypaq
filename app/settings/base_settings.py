from pydantic import BaseSettings
from functools import lru_cache

class BaseSetting(BaseSettings):
    app_name:str = "studypaq"
    user_name:str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return BaseSetting()