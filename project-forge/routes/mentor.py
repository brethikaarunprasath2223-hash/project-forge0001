"""routes/mentor.py — browse mentors and AI style mentor chat"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

from routes.helpers import login_required
from models.mentor import (
    get_all_mentors,
    get_mentor_by_id,
    request_mentorship,
    get_requests_for_student
)


mentor_bp = Blueprint("mentor", __name__)


# ================= Mentor List =================

@mentor_bp.route("/mentors")
@login_required
def mentors():

    all_mentors = get_all_mentors()

    my_requests = get_requests_for_student(
        session["user_id"]
    )

    requested_mentor_ids = {
        r["mentor_id"]
        for r in my_requests
    }


    return render_template(
        "mentor.html",
        mentors=all_mentors,
        requests=my_requests,
        requested_mentor_ids=requested_mentor_ids
    )



# ================= Request Mentor =================

@mentor_bp.route("/mentors/<int:mentor_id>/request", methods=["POST"])
@login_required
def request_mentor(mentor_id):

    mentor = get_mentor_by_id(mentor_id)


    if not mentor:
        flash(
            "Mentor not found.",
            "error"
        )
        return redirect(
            url_for("mentor.mentors")
        )


    message = request.form.get(
        "message",
        ""
    ).strip()


    request_mentorship(
        session["user_id"],
        mentor_id,
        None,
        message
    )


    flash(
        f"Your request has been sent to {mentor['name']}!",
        "success"
    )


    return redirect(
        url_for("mentor.mentors")
    )



# ================= AI Human Mentor Chat =================


@mentor_bp.route("/mentor/chat", methods=["POST"])
def mentor_chat():

    data = request.json

    question = data.get(
        "question",
        ""
    ).lower()



    if "project" in question:

        reply = """
👨‍🏫 Good project idea!

First prepare:

1. Problem statement
2. Requirements
3. Modules
4. Technology stack
5. Development roadmap

Build step by step.
"""


    elif "python" in question:

        reply = """
👨‍🏫 For Python projects:

Start with:
- Python basics
- Flask
- Database
- Testing

Then develop each module.
"""


    elif "error" in question or "bug" in question:

        reply = """
👨‍🏫 Don't worry about errors.

Send:
1. Error message
2. Code section
3. What you tried

I will help you debug.
"""


    elif "ai" in question:

        reply = """
👨‍🏫 AI project steps:

1. Dataset collection
2. Data cleaning
3. Model selection
4. Training
5. Testing
"""


    else:

        reply = """
👨‍🏫 I am your Project Forge Mentor.

Ask me about:
- Project ideas
- Coding errors
- Technology selection
- Development roadmap

I will guide you step by step.
"""



    return jsonify({
        "reply": reply
    })