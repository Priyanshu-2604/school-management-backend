# app/core/config.py

import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

load_dotenv()  # Load environment variables from a .env file if available

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Database
DATABASE_CONFIG = {
    'drivername': 'postgresql',
    'username': os.getenv("POSTGRES_USER", "user"),
    'password': os.getenv("POSTGRES_PASSWORD", "password"),
    'host': os.getenv("POSTGRES_HOST", "localhost"),
    'port': os.getenv("POSTGRES_PORT", "5432"),
    'database': os.getenv("POSTGRES_DB", "school_db"),
}

DATABASE_URL = str(URL.create(**DATABASE_CONFIG))
