# Project Forge

An AI-powered web app that turns a student's one-line project idea into a complete,
structured project plan — title, abstract, tech stack, roadmap, cost/time estimate,
and a beginner-friendly step-by-step build guide — plus mentor matching and
progress tracking.

Built with **Python Flask, HTML/CSS/JavaScript, and SQLite/MySQL.**

---

## 1. Project Architecture

```
Browser (HTML/CSS/JS, glassmorphism UI)
        │  HTTP (Flask routes, session-based auth)
        ▼
Flask App (app.py)
  ├── routes/        → Blueprints: auth, dashboard, project, mentor, feedback, profile
  ├── services/       → ai_generator.py — turns idea text into a structured project plan
  ├── models/         → Data access layer (users, projects, mentors, feedback)
  └── database/       → db.py (connection), schema.sql (tables)
        │
        ▼
SQLite (dev, zero-config) or MySQL (production)
```

**Request flow for the core feature (idea → project plan):**
1. Student submits idea text via `POST /generate-project`.
2. `services/ai_generator.py` detects the domain (AI/ML, Web, Mobile, IoT, General)
   from keywords, then builds a full structured plan from domain-specific templates.
3. The plan is saved to the `projects` table (`models/project.py`) and a `user_progress`
   row is created.
4. The student is redirected to `/project/<id>`, which renders every generated field
   plus a step-by-step development guide.

## 2. Folder Structure

```
project-forge/
├── app.py                  # App factory, blueprint registration, DB init
├── requirements.txt
├── database/
│   ├── db.py                # get_db_connection(), init_db() — SQLite or MySQL
│   └── schema.sql            # All table definitions + comments for MySQL port
├── models/
│   ├── user.py                # users table access + password hashing
│   ├── project.py             # projects + user_progress table access
│   └── mentor.py              # mentors, mentor_requests, feedback table access
├── routes/
│   ├── helpers.py             # @login_required decorator
│   ├── auth.py                 # welcome, register, login, logout
│   ├── dashboard.py            # main dashboard
│   ├── project.py              # idea submission, AI generation, project results
│   ├── mentor.py                # browse mentors, request mentorship
│   ├── feedback.py              # feedback submission
│   └── profile.py               # profile, settings, dark mode, tutorial state
├── services/
│   └── ai_generator.py         # the "AI" — domain detection + structured plan generation
├── templates/                  # Jinja2 templates (see below)
└── static/
    ├── css/style.css           # glassmorphism theme, dark/light mode, animations
    └── js/
        ├── main.js              # theme toggle, mobile sidebar, idea chips
        └── tutorial.js           # AI Guide onboarding tutorial engine
```

## 3. Database Schema

See `database/schema.sql` for full definitions. Summary:

| Table            | Purpose                                                         |
|-------------------|------------------------------------------------------------------|
| `users`            | Student accounts (name, email, college, dept, year, password hash) |
| `projects`          | Every generated project plan, stored field-by-field (JSON-encoded lists) |
| `mentors`            | Seeded mentor directory (skills, bio, rating, availability)        |
| `mentor_requests`     | Student → mentor mentorship requests + status                       |
| `feedback`             | User comments/suggestions + star rating                              |
| `user_progress`         | Per-project progress stage (idea_submitted → completed)               |

The app runs on **SQLite by default** (`project_forge.db`, auto-created on first run —
perfect for local dev and Replit). To use **MySQL** in production, set:

```bash
export USE_MYSQL=true
export MYSQL_HOST=your-host
export MYSQL_USER=your-user
export MYSQL_PASSWORD=your-password
export MYSQL_DATABASE=project_forge
```

and install `mysql-connector-python` (already in `requirements.txt`).

## 4. How the "AI" Generation Works

`services/ai_generator.py` uses keyword-based domain detection (AI/ML, Web, Mobile,
IoT, General) plus templated generation — so the app works fully offline with **zero
API keys**, which keeps it simple to run on Replit or anywhere else.

**To upgrade to real LLM-generated content** (more nuanced titles/abstracts), swap
the body of `generate_project()` to call the Anthropic API — the function signature
and return shape are already documented in the file's docstring, so nothing else in
the app needs to change.

## 5. How to Run Locally

```bash
# 1. Clone/unzip the project, then:
cd project-forge
pip install -r requirements.txt

# 2. Run it
python app.py
```

Visit **http://127.0.0.1:5000**. The SQLite database and all tables (plus 5 sample
mentors) are created automatically on first run — no manual setup needed.

## 6. How to Deploy

**Replit (recommended for quick submission/demo):**
1. Create a new Replit → Import from GitHub, or upload this folder as a zip.
2. Replit auto-detects `requirements.txt` and installs dependencies.
3. Set the Run command to `python app.py` (already reads the `PORT` env var Replit provides).
4. Click Run — Replit gives you a public URL.

**Render / PythonAnywhere / any VPS:**
1. Set `SECRET_KEY` as an environment variable (don't use the dev default in production).
2. For MySQL, set the `USE_MYSQL` + `MYSQL_*` variables shown above.
3. Use a production WSGI server instead of Flask's dev server, e.g.:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

## 7. Future Improvements

- Swap the rule-based generator for a real LLM call (Anthropic/OpenAI) for richer,
  more specific abstracts and problem statements.
- Real AI-generated architecture diagrams (currently a styled icon placeholder) via
  an image-generation API.
- Auto-export generated projects as downloadable Word/PDF documentation and PPT files.
- Real-time mentor chat instead of one-way request messages.
- Admin dashboard for reviewing feedback and mentor request volume.

---

Built for college students, by design: no external accounts, no paid APIs required
to run the whole thing end-to-end.
