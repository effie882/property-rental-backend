import os
from dotenv import load_dotenv

# Force .env values to override any existing shell environment variables
load_dotenv(override=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    _database_url = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    # strip surrounding whitespace and quotes (some providers inject quotes)
    _database_url = _database_url.strip().strip('"').strip("'")
    if _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)

    # verify the URL can be parsed by SQLAlchemy; fallback to sqlite on error
    try:
        from sqlalchemy.engine import make_url

        make_url(_database_url)
        SQLALCHEMY_DATABASE_URI = _database_url
    except Exception:
        # if parsing fails, default to sqlite to avoid crashing the app during startup
        SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "dev-jwt-secret"