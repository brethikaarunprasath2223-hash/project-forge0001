"""routes/auth.py — welcome page, registration, login, logout."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models.user import (
    create_user,
    get_user_by_email,
    verify_password
)

auth_bp = Blueprint("auth", __name__)


DEPARTMENTS = [
    "Computer Science and Engineering",
    "Information Technology",
    "Electronics and Communication Engineering",
    "Electrical and Electronics Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Artificial Intelligence and Data Science",
    "Biomedical Engineering",
    "Other",
]

YEARS = [
    "1st Year",
    "2nd Year",
    "3rd Year",
    "4th Year"
]


@auth_bp.route("/")
def welcome():
    if session.get("user_id"):
        return redirect(url_for("dashboard.dashboard"))

    return render_template("welcome.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        college_name = request.form.get("college_name", "").strip()
        department = request.form.get("department", "").strip()
        year = request.form.get("year", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")


        if not all([
            full_name,
            email,
            phone,
            college_name,
            department,
            year,
            password
        ]):
            flash("Please fill all fields.", "error")
            return render_template(
                "register.html",
                departments=DEPARTMENTS,
                years=YEARS,
                form={}
            )


        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template(
                "register.html",
                departments=DEPARTMENTS,
                years=YEARS,
                form=request.form
            )
        if password != confirm_password:
           flash("Passwords do not match.", "error")
           return render_template(
            "register.html",
           departments=DEPARTMENTS,
           years=YEARS,
           form=request.form
     )

        user_id, error = create_user(
            full_name,
            email,
            phone,
            college_name,
            department,
            year,
            password
        )


        if error:
            flash(error, "error")
            return render_template(
                "register.html",
                departments=DEPARTMENTS,
                years=YEARS,
                form=request.form
            )


        session["user_id"] = user_id
        session["full_name"] = full_name

        return redirect(url_for("dashboard.dashboard"))


    return render_template(
        "register.html",
        departments=DEPARTMENTS,
        years=YEARS,
        form={}

    )



@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")


        user = get_user_by_email(email)


        print("LOGIN USER:", user)


        if not user:
            flash("Invalid email or password.", "error")
            return render_template("login.html")


        if not verify_password(
            password,
            user["password_hash"]
        ):
            flash("Invalid email or password.", "error")
            return render_template("login.html")


        session["user_id"] = user["id"]
        session["full_name"] = user["full_name"]

        print("LOGIN USER ID:", user["id"])
        print("LOGIN NAME:", user["full_name"])

        return redirect(
            url_for("dashboard.dashboard")
        )


    return render_template("login.html")



@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(
        "You've been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.welcome")
    )