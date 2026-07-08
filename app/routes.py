from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.decorators import (
    super_admin_required,
    election_officer_required,
    student_required,
)
from flask import session
from app import db
from app.forms.auth_forms import RegisterForm, LoginForm
from app.forms.faculty_forms import FacultyForm
from app.forms.department_form import DepartmentForm
from app.models.user import User
from flask import request
from app.models.audit_log import AuditLog
from app.models.faculty import Faculty
from app.models.department import Department
from sqlalchemy import or_


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
            role="STUDENT"
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

            session.permanent = True
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
            if user.role == User.SUPER_ADMIN:
                return redirect(url_for("main.admin_dashboard"))
            
            elif user.role == User.ELECTION_OFFICER:
                return redirect(url_for("main.officer_dashboard"))

            elif user.role == User.STUDENT:
                return redirect(url_for("main.dashboard"))

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
@student_required
def dashboard():

    stats = {
        "upcoming": 0,
        "active": 0,
        "completed": 0,
        "voted": False
    }

    return render_template(
        "dashboard.html",
        stats=stats
    )

@main.route("/admin/dashboard")
@login_required
@super_admin_required
def admin_dashboard():

    total_students = User.query.filter_by(role=User.STUDENT).count()

    total_officers = User.query.filter_by(
        role=User.ELECTION_OFFICER
    ).count()

    total_admins = User.query.filter_by(
        role=User.SUPER_ADMIN
    ).count()

    stats = {
        "students": total_students,
        "officers": total_officers,
        "admins": total_admins,
        "elections": 0,
        "candidates": 0,
        "votes": 0
    }

    return render_template(
        "admin_dashboard.html",
        stats=stats
    )
from sqlalchemy import or_

@main.route("/admin/users")
@login_required
@super_admin_required
def manage_users():

    search = request.args.get("search", "").strip()

    role = request.args.get("role", "").strip()

    query = User.query

    if search:

        query = query.filter(

            or_(
                User.full_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.student_id.ilike(f"%{search}%")
            )

        )

    if role:

        query = query.filter(User.role == role)

    users = query.order_by(User.id.desc()).all()

    return render_template(
        "admin/users.html",
        users=users,
        search=search,
        role=role,
        User=User
    )
@main.route("/admin/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@super_admin_required
def edit_user(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == "POST":

        role = request.form.get("role")

        if role in [
            User.STUDENT,
            User.ELECTION_OFFICER,
            User.SUPER_ADMIN
        ]:

            user.role = role

            db.session.commit()

            flash(
                "User role updated successfully.",
                "success"
            )

            return redirect(url_for("main.manage_users"))

        flash(
            "Invalid role selected.",
            "danger"
        )

    return render_template(
        "admin/edit_user.html",
        user=user,
        User=User
    )

@main.route("/admin/users/<int:user_id>/toggle-status")
@login_required
@super_admin_required
def toggle_user_status(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent admin from disabling own account
    if user.id == current_user.id:

        flash(
            "You cannot deactivate your own account.",
            "danger"
        )

        return redirect(url_for("main.manage_users"))

    # Toggle status
    user.is_active_user = not user.is_active_user

    db.session.commit()

    if user.is_active_user:

        flash(
            "User activated successfully.",
            "success"
        )

    else:

        flash(
            "User deactivated successfully.",
            "warning"
        )

    return redirect(url_for("main.manage_users"))

@main.route("/admin/users/<int:user_id>/delete")
@login_required
@super_admin_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent deleting yourself
    if user.id == current_user.id:

        flash(
            "You cannot delete your own account.",
            "danger"
        )

        return redirect(url_for("main.manage_users"))

    db.session.delete(user)
    db.session.commit()

    flash(
        "User deleted successfully.",
        "success"
    )

    return redirect(url_for("main.manage_users"))

    
@main.route("/officer/dashboard")
@login_required
@election_officer_required
def officer_dashboard():

    stats = {
        "elections": 0,
        "candidates": 0,
        "approved": 0,
        "pending": 0
    }

    return render_template(
        "officer_dashboard.html",
        stats=stats
    )

@main.route("/officer/elections")
@login_required
@election_officer_required
def manage_elections():

    return render_template("officer/manage_elections.html")


@main.route("/officer/candidates")
@login_required
@election_officer_required
def manage_candidates():

    return render_template("officer/manage_candidates.html")


@main.route("/officer/approvals")
@login_required
@election_officer_required
def candidate_approvals():

    return render_template("officer/candidate_approvals.html")


@main.route("/officer/reports")
@login_required
@election_officer_required
def officer_reports():

    return render_template("officer/reports.html")

# ==========================
# Faculty Management
# ==========================

@main.route("/admin/faculties")
@login_required
@super_admin_required
def faculties():

    search = request.args.get("search", "")
    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = Faculty.query

    if search:
        query = query.filter(
            Faculty.name.ilike(f"%{search}%")
        )

    if status == "active":
        query = query.filter(Faculty.is_active == True)

    elif status == "inactive":
        query = query.filter(Faculty.is_active == False)

    if search:
        query = query.filter(
            Faculty.name.ilike(f"%{search}%")
        )

    faculties = query.order_by(
        Faculty.is_active.desc(),
        Faculty.name.asc()
    ).all()

    stats = {
        "total": Faculty.query.count(),
        "active": Faculty.query.filter_by(is_active=True).count(),
        "inactive": Faculty.query.filter_by(is_active=False).count()
    }

    return render_template(
    "admin/faculties/index.html",
    faculties=faculties,
    search=search,
    status=status,
    stats=stats
    )

@main.route("/admin/faculties/create", methods=["GET", "POST"])
@login_required
@super_admin_required
def create_faculty():

    form = FacultyForm()

    if form.validate_on_submit():

        faculty = Faculty(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data
        )

        existing = Faculty.query.filter_by(name=form.name.data).first()

        if existing:

            flash(
                "Faculty already exists.",
                "warning"
            )

            return render_template(
                "admin/faculties/create.html",
                form=form
            )

        faculty = Faculty(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data
        )
        db.session.add(faculty)
        db.session.commit()

        flash(
            "Faculty created successfully.",
            "success"
        )

        return redirect(url_for("main.faculties"))
    return render_template(
        "admin/faculties/create.html",
        form=form
    )

@main.route("/admin/faculties/<int:faculty_id>/edit", methods=["GET", "POST"])
@login_required
@super_admin_required
def edit_faculty(faculty_id):

    faculty = Faculty.query.get_or_404(faculty_id)

    form = FacultyForm(obj=faculty)

    if form.validate_on_submit():

        existing_name = Faculty.query.filter(
            Faculty.name == form.name.data,
            Faculty.id != faculty.id
        ).first()

        if existing_name:

            flash("Faculty name already exists.", "warning")

            return render_template(
                "admin/faculties/edit.html",
                form=form,
                faculty=faculty
            )

        existing_code = Faculty.query.filter(
            Faculty.code == form.code.data,
            Faculty.id != faculty.id
        ).first()

        if existing_code:

            flash("Faculty code already exists.", "warning")

            return render_template(
                "admin/faculties/edit.html",
                form=form,
                faculty=faculty
            )

        faculty.name = form.name.data
        faculty.code = form.code.data
        faculty.description = form.description.data

        db.session.commit()

        flash("Faculty updated successfully.", "success")

        return redirect(url_for("main.faculties"))

    return render_template(
        "admin/faculties/edit.html",
        form=form,
        faculty=faculty
    )

@main.route("/admin/faculties/delete/<int:faculty_id>")
@login_required
@super_admin_required
def delete_faculty(faculty_id):

    faculty = Faculty.query.get_or_404(faculty_id)

    db.session.delete(faculty)
    db.session.commit()

    flash(
        "Faculty deleted successfully.",
        "success"
    )

    return redirect(
        url_for("main.faculties")
    )

@main.route("/admin/faculties/<int:faculty_id>/toggle")
@login_required
@super_admin_required
def toggle_faculty(faculty_id):

    faculty = Faculty.query.get_or_404(faculty_id)

    faculty.is_active = not faculty.is_active

    db.session.commit()

    if faculty.is_active:
        flash("Faculty activated successfully.", "success")
    else:
        flash("Faculty deactivated successfully.", "warning")

    return redirect(url_for("main.faculties"))

# ==========================
# DEPARTMENT
# ==========================

@main.route("/admin/departments")
@login_required
@super_admin_required
def departments():

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = Department.query

    if search:
        query = query.filter(
            or_(
                Department.name.ilike(f"%{search}%"),
                Department.code.ilike(f"%{search}%")
            )
        )

    if status == "active":
        query = query.filter_by(is_active=True)

    elif status == "inactive":
        query = query.filter_by(is_active=False)

    departments = query.order_by(
        Department.created_at.desc()
    ).all()

    stats = {
        "total": Department.query.count(),
        "active": Department.query.filter_by(is_active=True).count(),
        "inactive": Department.query.filter_by(is_active=False).count()
    }

    return render_template(
        "admin/departments/index.html",
        departments=departments,
        search=search,
        status=status,
        stats=stats
    )

@main.route("/admin/departments/create", methods=["GET", "POST"])
@login_required
@super_admin_required
def create_department():

    form = DepartmentForm()
    form.load_faculties()

    if form.validate_on_submit():

        department = Department(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data,
            faculty_id=form.faculty_id.data,
            is_active=form.is_active.data
        )

        db.session.add(department)
        db.session.commit()

        flash(
            "Department created successfully.",
            "success"
        )

        return redirect(
            url_for("main.departments")
        )

    return render_template(
        "admin/departments/create.html",
        form=form
    )

@main.route("/admin/departments/edit/<int:department_id>", methods=["GET", "POST"])
@login_required
@super_admin_required
def edit_department(department_id):

    department = Department.query.get_or_404(department_id)

    form = DepartmentForm(obj=department)
    form.load_faculties()

    if form.validate_on_submit():

        department.name = form.name.data
        department.code = form.code.data
        department.description = form.description.data
        department.faculty_id = form.faculty_id.data
        department.is_active = form.is_active.data

        db.session.commit()

        flash(
            "Department updated successfully.",
            "success"
        )

        return redirect(
            url_for("main.departments")
        )

    form.faculty_id.data = department.faculty_id

    return render_template(
        "admin/departments/edit.html",
        form=form,
        department=department
    )

@main.route("/admin/departments/delete/<int:id>")
@login_required
@super_admin_required
def delete_department(id):

    department = Department.query.get_or_404(id)

    db.session.delete(department)
    db.session.commit()

    flash(
        "Department deleted successfully.",
        "success"
    )

    return redirect(
        url_for("main.departments")
    )

@main.route("/admin/departments/toggle/<int:department_id>")
@login_required
@super_admin_required
def toggle_department(department_id):

    department = Department.query.get_or_404(department_id)

    department.is_active = not department.is_active

    db.session.commit()

    flash(
        "Department status updated.",
        "success"
    )

    return redirect(
        url_for("main.departments")
    )



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

    session.clear()
    logout_user()

    flash(
        "You have successfully logged out.",
        "success"
    )

    return redirect(url_for("main.home"))

@main.route("/admin-test")
@super_admin_required
def admin_test():

    return "<h2>✅ Super Admin Access Granted</h2>"


@main.route("/officer-test")
@election_officer_required
def officer_test():

    return "<h2>✅ Election Officer Access Granted</h2>"


@main.route("/student-test")
@student_required
def student_test():

    return "<h2>✅ Student Access Granted</h2>"
   