"""
database/db.py
----------------
Handles the database connection for Project Forge.

By default this uses SQLite (file: project_forge.db) so the app runs
anywhere with zero setup (including Replit). To switch to MySQL for
production, set USE_MYSQL=true as an environment variable and fill in
the MYSQL_* variables — see README for details.
"""

import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "project_forge.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"

USE_MYSQL = os.environ.get("USE_MYSQL", "false").lower() == "true"


def get_db_connection():
    """
    Returns a database connection.
    SQLite is used by default (dev/Replit-friendly).
    If USE_MYSQL=true, a MySQL connection is returned instead
    (requires `mysql-connector-python` to be installed).
    """
    if USE_MYSQL:
        import mysql.connector  # imported lazily so SQLite mode never needs this package
        conn = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database=os.environ.get("MYSQL_DATABASE", "project_forge"),
        )
        return conn

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Creates all tables if they do not already exist, and seeds sample mentors."""
    conn = get_db_connection()
    cur = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    if USE_MYSQL:
        for statement in schema_sql.split(";"):
            statement = statement.strip()
            if statement:
                cur.execute(statement)
    else:
        conn.executescript(schema_sql)

    conn.commit()

    # Seed mentors only if table is empty
    cur.execute("SELECT COUNT(*) as c FROM mentors")
    row = cur.fetchone()
    count = row["c"] if not USE_MYSQL else row[0]

    if count == 0:
        seed_mentors(conn)

    conn.close()


def seed_mentors(conn):
    import json
    mentors = [
        ("Dr. Ananya Rao", "AI & Machine Learning Mentor",
         json.dumps(["Python", "TensorFlow", "Computer Vision", "NLP"]),
         "15+ years in AI research, guided 100+ student capstone projects.",
         "ananya.rao@mentors.dev", 4.9, "Available"),
        ("Karthik Subramaniam", "Full Stack Web Development Mentor",
         json.dumps(["React", "Node.js", "Flask", "MySQL", "REST APIs"]),
         "Ex-startup CTO, loves helping students ship real products.",
         "karthik.s@mentors.dev", 4.8, "Available"),
        ("Priya Menon", "Mobile App Development Mentor",
         json.dumps(["Flutter", "Kotlin", "Firebase", "UI/UX"]),
         "Published 6 apps on Play Store, mentors app-based final year projects.",
         "priya.menon@mentors.dev", 4.7, "Busy"),
        ("Rahul Verma", "IoT & Embedded Systems Mentor",
         json.dumps(["Arduino", "Raspberry Pi", "Sensors", "C/C++"]),
         "Hardware engineer specializing in smart-device student projects.",
         "rahul.verma@mentors.dev", 4.6, "Available"),
        ("Sneha Iyer", "Cybersecurity & Cloud Mentor",
         json.dumps(["AWS", "Network Security", "Docker", "DevOps"]),
         "Cloud security consultant, helps with deployment & security reviews.",
         "sneha.iyer@mentors.dev", 4.8, "Available"),
    ]
    conn.executemany(
        """INSERT INTO mentors (name, title, skills, bio, email, rating, availability)
           VALUES (?, ?, ?, ?, ?, ?, ?)""" if not USE_MYSQL else
        """INSERT INTO mentors (name, title, skills, bio, email, rating, availability)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        mentors,
    )
    conn.commit()
