import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(
    BASE_DIR,
    "project_forge.db"
)


def get_db_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn



def init_db():
    def init_db():

    conn = get_db_connection()

    conn.execute("DROP TABLE IF EXISTS projects")

   
for column in columns:
    try:
        conn.execute(
            f"ALTER TABLE projects ADD COLUMN {column} TEXT"
        )
    except sqlite3.OperationalError:
        pass

    conn = get_db_connection()

    schema_path = os.path.join(
        os.path.dirname(__file__),
        "schema.sql"
    )

    with open(schema_path, "r") as file:
        conn.executescript(file.read())
    # Migration: add missing columns
    try:
        conn.execute(
            "ALTER TABLE projects ADD COLUMN idea_text TEXT"
        )
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
    columns = [
    "idea_text",
    "problem_statement",
    "objectives",
    "features",
    "advantages",
    "disadvantages",
    "similar_projects",
    "suggested_improvements",
    "future_scope",
    "estimated_cost",
    "estimated_duration",
    "difficulty_level",
    "required_software",
    "required_hardware",
    "domain",
    "status"
]

for column in columns:
    try:
        conn.execute(
            f"ALTER TABLE projects ADD COLUMN {column} TEXT"
        )
    except sqlite3.OperationalError:
        pass