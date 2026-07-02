from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "fallback_secret_key"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///cems.db"
    )

    # Flask Session Security

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False      # Change to True after HTTPS deployment

    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True

    REMEMBER_COOKIE_SECURE = False

    REMEMBER_COOKIE_DURATION = timedelta(days=7)

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)