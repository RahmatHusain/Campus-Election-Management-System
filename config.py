import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key_123456")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'cems.db'}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    