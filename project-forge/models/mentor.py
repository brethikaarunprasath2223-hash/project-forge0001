"""models/mentor.py — data access for mentors, mentor_requests, feedback."""

import json
from database.db import get_db_connection


def get_all_mentors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mentors ORDER BY rating DESC")
    rows = cur.fetchall()
    conn.close()
    mentors = []
    for r in rows:
        m = dict(r)
        try:
            m["skills"] = json.loads(m["skills"])
        except (json.JSONDecodeError, TypeError):
            m["skills"] = []
        mentors.append(m)
    return mentors


def get_mentor_by_id(mentor_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mentors WHERE id = ?", (mentor_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    m = dict(row)
    try:
        m["skills"] = json.loads(m["skills"])
    except (json.JSONDecodeError, TypeError):
        m["skills"] = []
    return m


def request_mentorship(student_id, mentor_id, project_id, message):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO mentor_requests (student_id, mentor_id, project_id, message)
           VALUES (?, ?, ?, ?)""",
        (student_id, mentor_id, project_id, message),
    )
    conn.commit()
    conn.close()


def get_requests_for_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT mr.*, m.name as mentor_name, m.title as mentor_title FROM mentor_requests mr
           JOIN mentors m ON mr.mentor_id = m.id
           WHERE mr.student_id = ? ORDER BY mr.created_at DESC""",
        (student_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def submit_feedback(user_id, message, rating):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO feedback (user_id, message, rating) VALUES (?, ?, ?)",
        (user_id, message, rating),
    )
    conn.commit()
    conn.close()


def get_all_feedback(limit=20):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT f.*, u.full_name FROM feedback f
           LEFT JOIN users u ON f.user_id = u.id
           ORDER BY f.created_at DESC LIMIT ?""",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
