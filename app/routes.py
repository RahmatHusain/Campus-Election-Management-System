from datetime import datetime, timedelta
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
from flask import request
from app.models.audit_log import AuditLog
main = Blueprint("main", __name__)


# ==========================
# Home
# ==========================
@main.route("/")
def home():
    return render_template("index.html")


# ==========================
# Register
# ==========================
@main.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data.strip().lower()).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("main.register"))

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
        log = AuditLog(
            user_id=user.id,
            action="User Registered",
            ip_address=request.remote_addr
        )

        db.session.add(log)
        db.session.commit()

        flash("Registration successful!", "success")

        return redirect(url_for("main.login"))

    return render_template(
        "auth/register.html",
        form=form
    )


# ==========================
# Login
# ==========================
@main.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        # Account locked
        if user and user.account_locked_until:

            if user.account_locked_until > datetime.utcnow():

                remaining = (
                    user.account_locked_until - datetime.utcnow()
                ).seconds // 60

                flash(
                    f"Account locked. Try again in {remaining} minutes.",
                    "danger"
                )

                return redirect(url_for("main.login"))

            else:

                user.failed_login_attempts = 0
                user.account_locked_until = None
                db.session.commit()

        # Inactive account
        if user and hasattr(user, "is_active_user") and not user.is_active_user:

            flash(
                "Your account has been disabled.",
                "danger"
            )

            return redirect(url_for("main.login"))

        # Correct password
        if user and user.check_password(form.password.data):

            user.failed_login_attempts = 0
            user.account_locked_until = None
            user.last_login = datetime.utcnow()
            user.login_count += 1

            db.session.commit()

            login_user(
                user,
                remember=form.remember.data
            )
            log = AuditLog(
            user_id=user.id,
            action="User Logged In",
            ip_address=request.remote_addr
            )

            db.session.add(log)
            db.session.commit()

            flash(
                "Welcome back!",
                "success"
            )

            return redirect(url_for("main.dashboard"))

        # Wrong password
        else:

            if user:

                user.failed_login_attempts += 1

                if user.failed_login_attempts >= 5:

                    user.account_locked_until = (
                        datetime.utcnow() + timedelta(minutes=15)
                    )

                    flash(
                        "Too many failed login attempts. Account locked for 15 minutes.",
                        "danger"
                    )

                else:

                    remaining = 5 - user.failed_login_attempts

                    flash(
                        f"Invalid credentials. {remaining} attempts remaining.",
                        "warning"
                    )

                db.session.commit()

            else:

                flash(
                    "Invalid email or password.",
                    "danger"
                )

    return render_template(
        "auth/login.html",
        form=form
    )


# ==========================
# Dashboard
# ==========================
@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ==========================
# Profile
# ==========================
@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


# ==========================
# Logout
# ==========================
@main.route("/logout")
@login_required
def logout():

    current_user.last_logout = datetime.utcnow()

    log = AuditLog(
        user_id=current_user.id,
        action="User Logged Out",
        ip_address=request.remote_addr
    )

    db.session.add(log)
    db.session.commit()

    logout_user()

    flash(
        "You have successfully logged out.",
        "success"
    )

    return redirect(url_for("main.home"))