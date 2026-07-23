"""routes/project.py — idea submission, AI generation, project results, my projects."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from routes.helpers import login_required
from services.ai_generator import generate_project, generate_dev_guide
from models.project import save_project, get_project_by_id, get_projects_for_user, update_project_status

project_bp = Blueprint("project", __name__)


@project_bp.route("/submit-idea")
@login_required
def submit_idea():
    return render_template("submit_idea.html")


@project_bp.route("/generate-project", methods=["POST"])
@login_required
def generate():
    idea_text = request.form.get("idea_text", "").strip()
    if len(idea_text) < 10:
        flash("Please describe your idea in a bit more detail (at least a sentence or two).", "error")
        return redirect(url_for("project.submit_idea"))

    generated = generate_project(idea_text)
    project_id = save_project(session["user_id"], idea_text, generated)

    return redirect(url_for("project.view_project", project_id=project_id))


@project_bp.route("/project/<int:project_id>")
@login_required
def view_project(project_id):
    project = get_project_by_id(project_id)
    if not project or project["user_id"] != session["user_id"]:
        flash("Project not found.", "error")
        return redirect(url_for("project.my_projects"))

    dev_guide = generate_dev_guide(project)
    return render_template("project_result.html", project=project, dev_guide=dev_guide)


@project_bp.route("/my-projects")
@login_required
def my_projects():
    projects = get_projects_for_user(session["user_id"])
    return render_template("my_projects.html", projects=projects)


@project_bp.route("/project/<int:project_id>/status", methods=["POST"])
@login_required
def update_status(project_id):
    project = get_project_by_id(project_id)
    if not project or project["user_id"] != session["user_id"]:
        return jsonify({"success": False}), 404

    new_status = request.form.get("status", "saved")
    update_project_status(project_id, new_status)
    return jsonify({"success": True, "status": new_status})
