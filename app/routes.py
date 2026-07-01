from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app import db
from app.forms.auth_forms import RegisterForm, LoginForm
from app.models.user import User

# Create Blueprint HERE
main = Blueprint("main", __name__)

@main.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        # Check duplicate email
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("main.register"))

        # Check duplicate student ID
        if User.query.filter_by(student_id=form.student_id.data).first():
            flash("Student ID already exists.", "danger")
            return redirect(url_for("main.register"))

        user = User(
            full_name=form.full_name.data,
            student_id=form.student_id.data,
            email=form.email.data.strip().lower(),
            )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful!", "success")

        return redirect(url_for("main.home"))

    return render_template(
        "auth/register.html",
        form=form
    )
@main.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        user = User.query.filter_by(email=email).first()
        if user and not user.is_active_user:
            flash(
                "Your account has been disabled. Please contact the administrator.",
                "danger"
                )
            return redirect(url_for("main.login"))

        if user and user.check_password(form.password.data):

            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(
                user,
                remember=form.remember.data
            )

            flash(
                "Welcome back!",
                "success"
            )

            return redirect(url_for("main.dashboard"))

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )

@main.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(url_for("main.login"))
@main.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")

@main.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )

@main.route("/")
def home():
    return render_template("index.html")
