import os
import dotenv
from base_settings import get_settings

DEBUG = False

settings = get_settings()

# dotenv.load_dotenv(".env")

# DATABASE_URL = os.getenv("SQLALCHEMY_POSTGRES_DATABASE_URL")

print(dir(settings.SQLALCHEMY_DATABASE_URL))

