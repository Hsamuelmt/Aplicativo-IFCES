import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # --- Database Configuration ---
    # Prioritizes DATABASE_URL for production deployments like Render.
    # Falls back to a local MySQL setup and finally SQLite for development.

    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")

    mysql_url = None
    # Check if the essential DB variables are present to attempt a MySQL connection
    if DB_NAME and DB_USER:
        mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD or ''}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

    # SQLite fallback configuration
    SQLITE_PATH = BASE_DIR / "instance" / "app.db"
    SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    sqlite_url = f"sqlite:///{SQLITE_PATH.as_posix()}"

    # Set the final database URI
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or mysql_url or sqlite_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Uploads
    INSTANCE_PATH = BASE_DIR / "instance"
    UPLOAD_FOLDER = INSTANCE_PATH / "uploads"
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB max upload size

class TestConfig(Config):
    TESTING = True
    # Use a separate in-memory SQLite DB for tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"