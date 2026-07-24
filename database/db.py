import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "project_forge.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    # Reset old database tables (development only)
    conn.execute("DROP TABLE IF EXISTS user_progress")
    conn.execute("DROP TABLE IF EXISTS projects")

    schema_path = os.path.join(
        os.path.dirname(__file__),
        "schema.sql"
    )

    with open(schema_path, "r") as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()