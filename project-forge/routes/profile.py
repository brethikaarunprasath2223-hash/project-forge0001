"""routes/profile.py — user profile and settings."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from routes.helpers import login_required
from models.user import get_user_by_id, update_profile, toggle_dark_mode, mark_tutorial_seen
from models.project import get_projects_for_user, get_progress_for_user

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def profile():
    user = get_user_by_id(session["user_id"])
    projects = get_projects_for_user(session["user_id"])
    progress = get_progress_for_user(session["user_id"])

    saved_projects = [p for p in projects if p["status"] in ("saved", "in_progress", "completed")]

    return render_template("profile.html", user=user, projects=projects,
                            saved_projects=saved_projects, progress=progress)


@profile_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = get_user_by_id(session["user_id"])

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        college_name = request.form.get("college_name", "").strip()
        department = request.form.get("department", "").strip()
        year = request.form.get("year", "").strip()

        update_profile(session["user_id"], full_name, phone, college_name, department, year)
        session["full_name"] = full_name
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.settings"))

    return render_template("settings.html", user=user)


@profile_bp.route("/settings/dark-mode", methods=["POST"])
@login_required
def dark_mode():
    enabled = request.json.get("enabled", False)
    toggle_dark_mode(session["user_id"], enabled)
    return jsonify({"success": True})


@profile_bp.route("/tutorial/complete", methods=["POST"])
@login_required
def complete_tutorial():
    mark_tutorial_seen(session["user_id"])
    return jsonify({"success": True})
