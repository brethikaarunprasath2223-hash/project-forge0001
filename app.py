"""
app.py — Project Forge
------------------------
Main Flask application entry point. Registers all blueprints, initializes
the database on first run, and defines a couple of small template filters
used across pages (e.g. converting JSON tech-stack dicts to display lists).

Run locally with:  python app.py
"""

import os
from flask import Flask

from database.db import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.project import project_bp
from routes.mentor import mentor_bp
from routes.feedback import feedback_bp
from routes.profile import profile_bp


def create_app():
    app = Flask(__name__)

    # Secret key: in production, set SECRET_KEY as an environment variable.
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me-in-production")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(profile_bp)

    # Initialize database + tables (safe to call every start — uses IF NOT EXISTS)
    with app.app_context():
        init_db()

    @app.context_processor
    def inject_user():
        """Makes `user` available in every template (sidebar, navbar) without
        every single route needing to fetch and pass it manually."""
        from flask import session
        from models.user import get_user_by_id
        user = None
        if session.get("user_id"):
            user = get_user_by_id(session["user_id"])
        return {"user": user}


    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template("error.html", code=500, message="Something went wrong on our end."), 500

    return app


app = create_app()

if __name__ == "__main__":
    # host 0.0.0.0 + PORT env var makes this Replit-friendly
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
