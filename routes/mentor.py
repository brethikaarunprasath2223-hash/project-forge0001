"""routes/mentor.py — browse mentors, request mentorship."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from routes.helpers import login_required
from models.mentor import get_all_mentors, get_mentor_by_id, request_mentorship, get_requests_for_student
from models.project import get_projects_for_user

mentor_bp = Blueprint("mentor", __name__)


@mentor_bp.route("/mentors")
@login_required
def mentors():
    all_mentors = get_all_mentors()
    my_requests = get_requests_for_student(session["user_id"])
    requested_mentor_ids = {r["mentor_id"] for r in my_requests}
    return render_template("mentor.html", mentors=all_mentors, requests=my_requests,
                            requested_mentor_ids=requested_mentor_ids)


@mentor_bp.route("/mentors/<int:mentor_id>/request", methods=["POST"])
@login_required
def request_mentor(mentor_id):
    mentor = get_mentor_by_id(mentor_id)
    if not mentor:
        flash("Mentor not found.", "error")
        return redirect(url_for("mentor.mentors"))

    message = request.form.get("message", "").strip()
    project_id = request.form.get("project_id") or None

    request_mentorship(session["user_id"], mentor_id, project_id, message)
    flash(f"Your request has been sent to {mentor['name']}! They'll respond soon.", "success")
    return redirect(url_for("mentor.mentors"))
