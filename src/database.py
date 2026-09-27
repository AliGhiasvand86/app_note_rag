# Database connection management

import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "app.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection