"""routes/feedback.py — feedback submission."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from routes.helpers import login_required
from models.mentor import submit_feedback, get_all_feedback

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        rating = request.form.get("rating", "5")
        if not message:
            flash("Please write a message before submitting.", "error")
        else:
            submit_feedback(session["user_id"], message, int(rating))
            flash("Thank you for your feedback! It helps us improve Project Forge.", "success")
        return redirect(url_for("feedback.feedback"))

    all_feedback = get_all_feedback()
    return render_template("feedback.html", feedback_list=all_feedback)
