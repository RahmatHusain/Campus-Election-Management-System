from flask import Blueprint, render_template, redirect, url_for, flash

from app import db
from app.forms.auth_forms import RegisterForm
from app.models.user import User

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


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
            email=form.email.data,
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