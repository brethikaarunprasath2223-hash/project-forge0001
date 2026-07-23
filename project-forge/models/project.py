"""models/project.py — data access for the projects table."""

import json
from database.db import get_db_connection


def save_project(user_id, idea_text, generated):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO projects (
            user_id, idea_text, title, abstract, problem_statement, objectives, features,
            advantages, disadvantages, similar_projects, suggested_improvements, future_scope,
            tech_stack, roadmap, estimated_cost, estimated_duration, difficulty_level,
            required_software, required_hardware, domain, status
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            user_id, idea_text, generated["title"], generated["abstract"], generated["problem_statement"],
            json.dumps(generated["objectives"]), json.dumps(generated["features"]),
            json.dumps(generated["advantages"]), json.dumps(generated["disadvantages"]),
            json.dumps(generated["similar_projects"]), json.dumps(generated["suggested_improvements"]),
            json.dumps(generated["future_scope"]), json.dumps(generated["tech_stack"]),
            json.dumps(generated["roadmap"]), generated["estimated_cost"], generated["estimated_duration"],
            generated["difficulty_level"], json.dumps(generated["required_software"]),
            json.dumps(generated["required_hardware"]), generated["domain"], "generated",
        ),
    )
    conn.commit()
    project_id = cur.lastrowid

    # Kick off progress tracking
    cur.execute(
        """INSERT INTO user_progress (user_id, project_id, stage, progress_percent)
           VALUES (?, ?, 'idea_submitted', 10)""",
        (user_id, project_id),
    )
    conn.commit()
    conn.close()
    return project_id


def _deserialize(row):
    d = dict(row)
    for field in ["objectives", "features", "advantages", "disadvantages", "similar_projects",
                  "suggested_improvements", "future_scope", "tech_stack", "roadmap",
                  "required_software", "required_hardware"]:
        if d.get(field):
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                pass
    return d


def get_project_by_id(project_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cur.fetchone()
    conn.close()
    return _deserialize(row) if row else None


def get_projects_for_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [_deserialize(r) for r in rows]


def update_project_status(project_id, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE projects SET status = ? WHERE id = ?", (status, project_id))
    conn.commit()
    conn.close()


def get_progress_for_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT up.*, p.title FROM user_progress up
           JOIN projects p ON up.project_id = p.id
           WHERE up.user_id = ? ORDER BY up.updated_at DESC""",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
