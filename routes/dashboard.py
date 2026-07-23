"""routes/dashboard.py — main dashboard after login."""

from flask import Blueprint, render_template, session, redirect, url_for
from models.user import get_user_by_id
from models.project import get_projects_for_user
from routes.helpers import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    user = get_user_by_id(session.get("user_id"))
    if not user:
        return redirect(url_for("auth.login"))

    projects = get_projects_for_user(user["id"])
    show_tutorial = not user.get("tutorial_seen")

    return render_template(
        "dashboard.html",
        user=user,
        projects=projects,
        project_count=len(projects),
        show_tutorial=show_tutorial,
    )
