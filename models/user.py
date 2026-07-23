"""models/user.py — data access for the users table."""

from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db_connection


def create_user(full_name, email, phone, college_name, department, year, password):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cur.execute(
            """INSERT INTO users (full_name, email, phone, college_name, department, year, password_hash)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (full_name, email, phone, college_name, department, year, password_hash),
        )
        conn.commit()
        user_id = cur.lastrowid
        return user_id, None
    except Exception as e:
        if "UNIQUE" in str(e) or "Duplicate" in str(e):
            return None, "An account with this email already exists."
        return None, "Something went wrong while creating your account."
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def verify_password(user, password):
    return check_password_hash(user["password_hash"], password)


def mark_tutorial_seen(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET tutorial_seen = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def toggle_dark_mode(user_id, enabled):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET dark_mode = ? WHERE id = ?", (1 if enabled else 0, user_id))
    conn.commit()
    conn.close()


def update_profile(user_id, full_name, phone, college_name, department, year):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """UPDATE users SET full_name=?, phone=?, college_name=?, department=?, year=?
           WHERE id=?""",
        (full_name, phone, college_name, department, year, user_id),
    )
    conn.commit()
    conn.close()
