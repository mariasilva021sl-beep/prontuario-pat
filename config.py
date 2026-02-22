import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _default_db_url():
    sqlite_path = os.path.join(BASE_DIR, "data", "app.db")
    return f"sqlite:///{sqlite_path}"


def _database_url():
    db_url = os.getenv("DATABASE_URL", _default_db_url())
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return db_url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
