import os
import dotenv
from .base_settings import *

DEBUG = False
dotenv.load_dotenv(".env")

DATABASE_URL = os.getenv("SQLALCHEMY_POSTGRES_DATABASE_URL")

print(DATABASE_URL)

