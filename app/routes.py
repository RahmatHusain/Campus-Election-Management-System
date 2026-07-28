from flask import jsonify
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
from app.decorators import role_required

from flask import session
from app import db
from app.forms.auth_forms import RegisterForm, LoginForm
from app.forms.faculty_forms import FacultyForm
from app.forms.department_form import DepartmentForm
from app.forms.semester_form import SemesterForm
from app.forms.election_form import ElectionForm
from app.forms.position_form import PositionForm
from app.services.position_service import PositionService
from app.models.position import Position
from app.forms.candidate_form import CandidateForm
from app.models.candidate import Candidate
from app.models.election import Election
from app.forms.program_form import (
    ProgramForm,
    EditProgramForm
)
import os
from app.models.user import User
from flask import request
from app.models.audit_log import AuditLog

from app.utils.audit import log_action
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.semester import Semester
from app.models.academic_year import AcademicYear
from app.models.program import Program
from app.forms.student_form import (
    StudentForm,
    EditStudentForm
)
from app.models.student import Student
from app.utils.student_id import (
    generate_student_id,
    generate_roll_number
)
from app.utils.file_upload import (
    save_student_photo,
    delete_student_photo
)
from app.forms.academic_year_forms import (
    AcademicYearForm,
    EditAcademicYearForm
)
from app.forms.bulk_form import BulkActionForm
from flask import send_file
from app.utils.student_import import import_students
from app.utils.student_export import export_students_to_excel
from app.utils.student_import import import_students as import_students_file
from io import BytesIO, StringIO
from app.forms.semester_form import (
    SemesterForm,
    EditSemesterForm
)



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
                entity_type="user",
                entity_id=user.id,
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

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "")
    faculty_id = request.args.get("faculty", "")

    query = Department.query

    # ------------------------
    # Search
    # ------------------------

    if search:
        query = query.filter(
            db.or_(
                Department.name.ilike(f"%{search}%"),
                Department.code.ilike(f"%{search}%")
            )
        )

    # ------------------------
    # Status Filter
    # ------------------------

    if status == "active":
        query = query.filter(Department.is_active == True)

    elif status == "inactive":
        query = query.filter(Department.is_active == False)

    # ------------------------
    # Faculty Filter
    # ------------------------

    if faculty_id:
        query = query.filter(
            Department.faculty_id == int(faculty_id)
        )

    departments = query.order_by(
        Department.name
    ).all()

    faculties = Faculty.query.order_by(
        Faculty.name
    ).all()

    stats = {
        "total": Department.query.count(),

        "active": Department.query.filter_by(
            is_active=True
        ).count(),

        "inactive": Department.query.filter_by(
            is_active=False
        ).count(),

        "faculties": Faculty.query.count(),
    }

    return render_template(
        "admin/departments/index.html",
        departments=departments,
        faculties=faculties,
        stats=stats,
        search=search,
        status=status,
        faculty_id=faculty_id
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

    try:
        db.session.delete(department)
        db.session.commit()

        flash(
            "Department deleted successfully.",
            "success"
        )

    except Exception:

        db.session.rollback()

        flash(
            "Unable to delete department. It may be linked with other records.",
            "danger"
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

# ==========================================
# Academic Year Management Routes
# ==========================================

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required

from app import db
from app.decorators import super_admin_required

from app.models.academic_year import AcademicYear


# ======================================================
# Academic Year List
# ======================================================

@main.route("/admin/academic-years")
@login_required
@super_admin_required
def academic_years():

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    query = AcademicYear.query

    if search:
        query = query.filter(
            AcademicYear.name.ilike(f"%{search}%")
        )

    if status == "active":
        query = query.filter(
            AcademicYear.is_active == True
        )

    elif status == "inactive":
        query = query.filter(
            AcademicYear.is_active == False
        )

    academic_years = query.order_by(
        AcademicYear.start_date.desc()
    ).all()

    stats = {
        "total": AcademicYear.query.count(),
        "active": AcademicYear.query.filter_by(is_active=True).count(),
        "inactive": AcademicYear.query.filter_by(is_active=False).count(),
        "current": AcademicYear.query.filter_by(is_current=True).count(),
    }

    return render_template(
        "admin/academic_years/index.html",
        academic_years=academic_years,
        stats=stats,
        search=search,
        status=status,
    )


# ======================================================
# Create Academic Year
# ======================================================

@main.route("/admin/academic-years/create", methods=["GET", "POST"])
@login_required
@super_admin_required
def create_academic_year():

    form = AcademicYearForm()

    if form.validate_on_submit():

        try:

            if form.is_current.data:
                AcademicYear.query.update(
                    {"is_current": False}
                )

            academic_year = AcademicYear(
                name=form.name.data.strip(),
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                is_current=form.is_current.data,
                is_active=form.is_active.data,
            )

            db.session.add(academic_year)
            db.session.commit()

            flash(
                "Academic Year created successfully.",
                "success",
            )

            return redirect(
                url_for("main.academic_years")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {e}",
                "danger",
            )

    return render_template(
        "admin/academic_years/create.html",
        form=form,
    )


# ======================================================
# Edit Academic Year
# ======================================================
@main.route("/admin/academic-years/edit/<int:id>", methods=["GET", "POST"])
@login_required
@super_admin_required
def edit_academic_year(id):

    academic_year = AcademicYear.query.get_or_404(id)

    form = EditAcademicYearForm(
        original_name=academic_year.name,
        obj=academic_year
    )

    if form.validate_on_submit():

        try:

            academic_year.name = form.name.data.strip()
            academic_year.start_date = form.start_date.data
            academic_year.end_date = form.end_date.data
            academic_year.is_active = form.is_active.data

            if form.is_current.data:

                AcademicYear.query.update(
                    {"is_current": False}
                )

                academic_year.is_current = True

            else:

                academic_year.is_current = False

            db.session.commit()

            flash(
                "Academic Year updated successfully.",
                "success"
            )

            return redirect(
                url_for("main.academic_years")
            )

        except Exception as e:

            db.session.rollback()

            flash(str(e), "danger")

    return render_template(
        "admin/academic_years/edit.html",
        form=form,
        academic_year=academic_year
    )
# ======================================================
# Set Current Academic Year
# ======================================================

@main.route("/admin/academic-years/current/<int:id>")
@login_required
@super_admin_required
def set_current_academic_year(id):

    try:

        AcademicYear.query.update(
            {"is_current": False}
        )

        academic_year = AcademicYear.query.get_or_404(id)

        academic_year.is_current = True
        academic_year.is_active = True

        db.session.commit()

        flash(
            f"{academic_year.name} is now the Current Academic Year.",
            "success",
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {e}",
            "danger",
        )

    return redirect(
        url_for("main.academic_years")
    )


# ======================================================
# Toggle Active / Inactive
# ======================================================

@main.route("/admin/academic-years/toggle/<int:id>")
@login_required
@super_admin_required
def toggle_academic_year(id):

    academic_year = AcademicYear.query.get_or_404(id)

    try:
        academic_year.is_active = not academic_year.is_active

        db.session.commit()

        flash(
            "Academic Year status updated successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {e}",
            "danger"
        )

    return redirect(
        url_for("main.academic_years")
    )


# ======================================================
# Delete Academic Year
# ======================================================
@main.route("/admin/academic-years/delete/<int:id>")
@login_required
@super_admin_required
def delete_academic_year(id):

    academic_year = AcademicYear.query.get_or_404(id)

    try:
        db.session.delete(academic_year)
        db.session.commit()

        flash(
            "Academic Year deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Delete failed: {str(e)}",
            "danger"
        )

    return redirect(
        url_for("main.academic_years")
    )

# ==========================
# Semesters
# ==========================

@main.route("/admin/semesters")
@login_required
@super_admin_required
def semesters():

    search = request.args.get("search", "").strip()

    academic_year_id = request.args.get("academic_year", "")

    status = request.args.get("status", "")

    query = Semester.query

    if search:
        query = query.filter(
            Semester.name.ilike(f"%{search}%")
        )

    if academic_year_id:
        query = query.filter_by(
            academic_year_id=academic_year_id
        )

    if status == "active":
        query = query.filter_by(is_active=True)

    elif status == "inactive":
        query = query.filter_by(is_active=False)

    semesters = query.order_by(
        Semester.semester_number
    ).all()

    stats = {
        "total": Semester.query.count(),
        "active": Semester.query.filter_by(is_active=True).count(),
        "inactive": Semester.query.filter_by(is_active=False).count(),
        "current": Semester.query.filter_by(is_current=True).count()
    }

    return render_template(
        "admin/semesters/index.html",
        semesters=semesters,
        stats=stats,
        search=search,
        status=status,
        academic_year_id=academic_year_id,
        academic_years=AcademicYear.query.all()
    )

@main.route("/admin/semesters/create", methods=["GET", "POST"])
@login_required
@super_admin_required
def create_semester():

    form = SemesterForm()

    if form.validate_on_submit():

        if form.is_current.data:
            Semester.query.update(
                {
                    "is_current": False
                    }
                    )
                    
            form.is_active.data = True

        try:

            if form.is_current.data:
                Semester.query.update(
                    {"is_current": False}
                )

            semester = Semester(
                academic_year_id=form.academic_year_id.data,
                name=form.name.data.strip(),
                semester_number=form.semester_number.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                is_current=form.is_current.data,
                is_active=form.is_active.data
            )

            db.session.add(semester)

            db.session.commit()

            flash(
                "Semester created successfully.",
                "success"
            )

            return redirect(
                url_for("main.semesters")
            )

        except Exception as e:

            db.session.rollback()

            flash(str(e), "danger")

    return render_template(
        "admin/semesters/create.html",
        form=form
    )

@main.route("/admin/semesters/toggle/<int:id>")
@login_required
@super_admin_required
def toggle_semester(id):

    semester = Semester.query.get_or_404(id)

    semester.is_active = not semester.is_active

    db.session.commit()

    flash(
        "Semester status updated successfully.",
        "success"
    )

    return redirect(
        url_for("main.semesters")
    )

# ==========================================
# Edit Semester
# ==========================================

@main.route('/admin/semesters/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@super_admin_required
def edit_semester(id):

    semester = Semester.query.get_or_404(id)

    # Load edit form with current semester data
    form = EditSemesterForm(
        semester.name,
        obj=semester
    )

    # IMPORTANT:
    # Pre-select current academic year in dropdown
    if request.method == 'GET':
        form.academic_year_id.data = semester.academic_year_id

    if form.validate_on_submit():

        try:

            # -----------------------------
            # Update semester fields
            # -----------------------------
            semester.academic_year_id = form.academic_year_id.data
            semester.name = form.name.data.strip()
            semester.semester_number = form.semester_number.data
            semester.start_date = form.start_date.data
            semester.end_date = form.end_date.data
            semester.is_current = form.is_current.data
            semester.is_active = form.is_active.data

            # -----------------------------
            # Ensure only one current semester
            # -----------------------------
            if semester.is_current:

                Semester.query.filter(
                    Semester.id != semester.id
                ).update(
                    {'is_current': False},
                    synchronize_session=False
                )

            db.session.commit()

            flash(
                'Semester updated successfully.',
                'success'
            )

            return redirect(
                url_for('main.semesters')
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f'Error updating semester: {str(e)}',
                'danger'
            )

    return render_template(
        'admin/semesters/edit.html',
        form=form,
        semester=semester
    )


# ==========================================
# Set Current Semester
# ==========================================

@main.route('/admin/semesters/current/<int:id>')
@login_required
@super_admin_required
def set_current_semester(id):

    try:

        # Remove current flag from all semesters
        Semester.query.update(
            {'is_current': False},
            synchronize_session=False
        )

        # Set selected semester as current
        semester = Semester.query.get_or_404(id)

        semester.is_current = True
        semester.is_active = True

        db.session.commit()

        flash(
            f'{semester.name} is now the current semester.',
            'success'
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f'Error setting current semester: {str(e)}',
            'danger'
        )

    return redirect(
        url_for('main.semesters')
    )

@main.route("/admin/semesters/delete/<int:id>")
@login_required
@super_admin_required
def delete_semester(id):

    semester = Semester.query.get_or_404(id)

    if semester.is_current:

        flash(
            "Current Semester cannot be deleted.",
            "danger"
        )

        return redirect(
            url_for("main.semesters")
        )

    db.session.delete(semester)

    db.session.commit()

    flash(
        "Semester deleted successfully.",
        "success"
    )

    return redirect(
        url_for("main.semesters")
    )

# ==========================
# Programs
# ==========================

@main.route("/admin/programs")
@login_required
@super_admin_required
def programs():

    search = request.args.get("search", "").strip()

    department_id = request.args.get("department", "")

    status = request.args.get("status", "")

    query = Program.query

    if search:

        query = query.filter(
            Program.name.ilike(f"%{search}%")
        )

    if department_id:

        query = query.filter_by(
            department_id=department_id
        )

    if status == "active":

        query = query.filter_by(
            is_active=True
        )

    elif status == "inactive":

        query = query.filter_by(
            is_active=False
        )

    programs = query.order_by(
        Program.name.asc()
    ).all()

    stats = {

        "total": Program.query.count(),

        "active": Program.query.filter_by(
            is_active=True
        ).count(),

        "inactive": Program.query.filter_by(
            is_active=False
        ).count(),

        "departments": Department.query.count()

    }

    return render_template(

        "admin/programs/index.html",

        programs=programs,

        stats=stats,

        departments=Department.query.order_by(
            Department.name
        ).all(),

        search=search,

        department_id=department_id,

        status=status

    )
@main.route( "/admin/programs/create", methods=["GET", "POST"] )
@login_required
@super_admin_required
def create_program():

    form = ProgramForm()

    if form.validate_on_submit():

        try:

            program = Program(

                department_id=form.department_id.data,

                name=form.name.data.strip(),

                code=form.code.data.strip().upper(),

                duration_years=form.duration_years.data,

                total_semesters=form.total_semesters.data,

                description=form.description.data,

                is_active=form.is_active.data

            )

            db.session.add(program)

            db.session.commit()

            flash(

                "Program created successfully.",

                "success"

            )

            return redirect(
                url_for("main.programs")
            )

        except Exception as e:

            db.session.rollback()

            flash(

                f"Error : {e}",

                "danger"

            )

    return render_template(

        "admin/programs/create.html",

        form=form

    )

@main.route( "/admin/programs/edit/<int:id>", methods=["GET", "POST"] )
@login_required
@super_admin_required
def edit_program(id):

    program = Program.query.get_or_404(id)

    form = EditProgramForm(program, obj=program)

    if request.method == "GET":

        form.department_id.data = program.department_id

    if form.validate_on_submit():

        try:

            program.department_id = form.department_id.data

            program.name = form.name.data.strip()

            program.code = form.code.data.strip().upper()

            program.duration_years = form.duration_years.data

            program.total_semesters = form.total_semesters.data

            program.description = form.description.data

            program.is_active = form.is_active.data

            db.session.commit()

            flash(

                "Program updated successfully.",

                "success"

            )

            return redirect(
                url_for("main.programs")
            )

        except Exception as e:

            db.session.rollback()

            flash(

                f"Error : {e}",

                "danger"

            )

    return render_template(

        "admin/programs/edit.html",

        form=form,

        program=program

    )

@main.route( "/admin/programs/toggle/<int:id>" )
@login_required
@super_admin_required
def toggle_program(id):

    program = Program.query.get_or_404(id)

    program.is_active = not program.is_active

    db.session.commit()

    flash(

        "Program status updated successfully.",

        "success"

    )

    return redirect(
        url_for("main.programs")
    )

@main.route( "/admin/programs/delete/<int:id>" )
@login_required
@super_admin_required
def delete_program(id):

    program = Program.query.get_or_404(id)

    try:

        db.session.delete(program)

        db.session.commit()

        flash(

            "Program deleted successfully.",

            "success"

        )

    except Exception as e:

        db.session.rollback()

        flash(

            f"Unable to delete Program : {e}",

            "danger"

        )

    return redirect(
        url_for("main.programs")
    )
# ==========================
# Programs
# ==========================
from app.forms.student_form import StudentForm, EditStudentForm
from app.utils.file_upload import save_student_photo, delete_student_photo
from app.forms.bulk_form import BulkActionForm
# ==========================================
# Student List (Advanced Search + Pagination)
# ==========================================
from sqlalchemy import or_

@main.route('/admin/students')
@login_required
@super_admin_required
def students():

    # -----------------------------
    # Query Parameters
    # -----------------------------
    search = request.args.get('search', '').strip()
    faculty_id = request.args.get('faculty', type=int)
    verified = request.args.get('verified', '')
    status = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)

    # -----------------------------
    # Base Query
    # -----------------------------
    query = Student.query

    # -----------------------------
    # Search
    # -----------------------------
    if search:

        query = query.filter(
            or_(
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%'),
                Student.student_id.ilike(f'%{search}%'),
                Student.roll_number.ilike(f'%{search}%'),
                Student.email.ilike(f'%{search}%')
            )
        )

    # -----------------------------
    # Faculty Filter
    # -----------------------------
    if faculty_id:

        query = query.filter(
            Student.faculty_id == faculty_id
        )

    # -----------------------------
    # Verification Filter
    # -----------------------------
    if verified == 'verified':

        query = query.filter(
            Student.is_verified.is_(True)
        )

    elif verified == 'unverified':

        query = query.filter(
            Student.is_verified.is_(False)
        )

    # -----------------------------
    # Status Filter
    # -----------------------------
    if status == 'active':

        query = query.filter(
            Student.is_active.is_(True)
        )

    elif status == 'inactive':

        query = query.filter(
            Student.is_active.is_(False)
        )

    # -----------------------------
    # Pagination
    # -----------------------------
       # Pagination
    students = query.order_by(Student.created_at.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    # Faculties for filter dropdown
    faculties = Faculty.query.order_by(Faculty.name).all()

    # Bulk action form
    bulk_form = BulkActionForm()

    # Statistics
    stats = {
        'total': Student.query.count(),
        'verified': Student.query.filter_by(is_verified=True).count(),
        'active': Student.query.filter_by(is_active=True).count(),
        'voters': Student.query.filter_by(is_voter=True).count()
    }

    return render_template(
        'admin/students/index.html',
        students=students,
        faculties=faculties,
        stats=stats,
        search=search,
        faculty_id=faculty_id,
        verified=verified,
        status=status,
        bulk_form=bulk_form
    )
@main.route('/admin/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@super_admin_required
def edit_student(id):

    # Get student
    student = Student.query.get_or_404(id)

    # Use edit form (fixes duplicate email issue)
    form = EditStudentForm(student, obj=student)

    # Process form submission
    if form.validate_on_submit():

        try:

            # ==========================
            # Handle Photo Upload
            # ==========================

            photo_file = form.photo.data

            # Upload only if a NEW file is selected
            if (
                photo_file
                and hasattr(photo_file, 'filename')
                and photo_file.filename
            ):

                # Delete old photo
                delete_student_photo(student.photo)

                # Save new photo
                student.photo = save_student_photo(photo_file)

            # ==========================
            # Update Personal Information
            # ==========================

            student.first_name = form.first_name.data.strip()
            student.last_name = form.last_name.data.strip()
            student.gender = form.gender.data
            student.date_of_birth = form.date_of_birth.data

            # ==========================
            # Update Contact Information
            # ==========================

            student.email = form.email.data.strip().lower()
            student.phone = form.phone.data.strip()
            student.address = form.address.data

            # ==========================
            # Update Academic Information
            # ==========================

            student.faculty_id = form.faculty_id.data
            student.department_id = form.department_id.data
            student.program_id = form.program_id.data
            student.academic_year_id = form.academic_year_id.data
            student.semester_id = form.semester_id.data

            student.admission_year = form.admission_year.data
            student.batch = form.batch.data

            # ==========================
            # Update Election Settings
            # ==========================

            student.is_voter = form.is_voter.data
            student.is_candidate_eligible = form.is_candidate_eligible.data
            student.is_verified = form.is_verified.data
            student.is_active = form.is_active.data

            # ==========================
            # Save Changes
            # ==========================

            db.session.commit()

            flash(
                f'Student {student.full_name} updated successfully.',
                'success'
            )

            return redirect(
                url_for('main.students')
            )

        except Exception as e:

            # Rollback database
            db.session.rollback()

            flash(
                f'Error: {str(e)}',
                'danger'
            )

    # Render edit page
    return render_template(
        'admin/students/edit.html',
        form=form,
        student=student
    )
# ==========================================
# Create Student
# ==========================================

@main.route('/admin/students/create', methods=['GET', 'POST'])
@login_required
@super_admin_required
def add_student():

    form = StudentForm()

    if form.validate_on_submit():

        try:

            # -----------------------------
            # Handle photo upload
            # -----------------------------
            photo_path = None

            if (
                form.photo.data and
                hasattr(form.photo.data, 'filename') and
                form.photo.data.filename
            ):
                photo_path = save_student_photo(
                    form.photo.data
                )

            # -----------------------------
            # Generate Student ID & Roll
            # -----------------------------
            admission_year = form.admission_year.data

            student_id = generate_student_id(
                form.program_id.data,
                admission_year
            )

            roll_number = generate_roll_number(
                form.program_id.data,
                admission_year
            )

            # -----------------------------
            # Create Student
            # -----------------------------
            student = Student(

                student_id=student_id,
                roll_number=roll_number,

                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),

                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data,

                email=form.email.data.strip().lower(),
                phone=form.phone.data.strip(),
                address=form.address.data,

                faculty_id=form.faculty_id.data,
                department_id=form.department_id.data,
                program_id=form.program_id.data,
                academic_year_id=form.academic_year_id.data,
                semester_id=form.semester_id.data,

                admission_year=admission_year,
                batch=form.batch.data,

                photo=photo_path,

                is_voter=form.is_voter.data,
                is_candidate_eligible=form.is_candidate_eligible.data,
                is_verified=form.is_verified.data,
                is_active=form.is_active.data
            )

            db.session.add(student)
            db.session.commit()

            flash(
                'Student created successfully.',
                'success'
            )

            return redirect(
                url_for('main.students')
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f'Error creating student: {str(e)}',
                'danger'
            )

    return render_template(
        'admin/students/create.html',
        form=form
    )

@main.route("/admin/students/delete/<int:id>")
@login_required
@super_admin_required
def delete_student(id):

    student = Student.query.get_or_404(id)

    try:

        # Delete photo
        delete_student_photo(student.photo)

        db.session.delete(student)
        db.session.commit()

        flash("Student deleted successfully.", "success")

    except Exception:

        db.session.rollback()

        flash("Unable to delete student.", "danger")

    return redirect(url_for("main.students"))
# ==========================================
# Bulk Student Actions
# ==========================================
@main.route('/admin/students/bulk-action', methods=['POST'])
@login_required
@super_admin_required
def bulk_student_action():

    student_ids = request.form.getlist('student_ids')
    action = request.form.get('action')

    if not student_ids:

        flash('Please select at least one student.', 'warning')

        return redirect(url_for('main.students'))

    try:

        students = Student.query.filter(
            Student.id.in_(student_ids)
        ).all()

        if not students:

            flash('No valid students selected.', 'danger')

            return redirect(url_for('main.students'))

        # -----------------------------
        # VERIFY
        # -----------------------------
        if action == 'verify':

            for student in students:

                student.is_verified = True

                log_action(
                    current_user.id,
                    'STUDENT_VERIFIED',
                    'Student',
                    student.id,
                    f'Bulk verified student {student.student_id}'
                )

            message = f'{len(students)} student(s) verified successfully.'

        # -----------------------------
        # ACTIVATE
        # -----------------------------
        elif action == 'activate':

            for student in students:

                student.is_active = True

                log_action(
                    current_user.id,
                    'STUDENT_ACTIVATED',
                    'Student',
                    student.id,
                    f'Bulk activated student {student.student_id}'
                )

            message = f'{len(students)} student(s) activated successfully.'

        # -----------------------------
        # DEACTIVATE
        # -----------------------------
        elif action == 'deactivate':

            for student in students:

                student.is_active = False

                log_action(
                    current_user.id,
                    'STUDENT_DEACTIVATED',
                    'Student',
                    student.id,
                    f'Bulk deactivated student {student.student_id}'
                )

            message = f'{len(students)} student(s) deactivated successfully.'

        # -----------------------------
        # DELETE
        # -----------------------------
        elif action == 'delete':

            count = len(students)

            for student in students:

                # Delete photo from filesystem
                if student.photo:

                    delete_student_photo(student.photo)

                log_action(
                    current_user.id,
                    'STUDENT_DELETED',
                    'Student',
                    student.id,
                    f'Bulk deleted student {student.student_id}'
                )

                db.session.delete(student)

            message = f'{count} student(s) deleted successfully.'

        else:

            flash('Invalid bulk action.', 'danger')

            return redirect(url_for('main.students'))

        db.session.commit()

        flash(message, 'success')

    except Exception as e:

        db.session.rollback()

        flash(f'Bulk operation failed: {str(e)}', 'danger')

    return redirect(url_for('main.students'))
@main.route('/admin/students/profile/<int:id>')
@login_required
@super_admin_required
def student_profile(id):

    student = Student.query.get_or_404(id)

    # Profile statistics
    profile_stats = {
        'is_verified': student.is_verified,
        'is_active': student.is_active,
        'is_voter': student.is_voter,
        'is_candidate_eligible': student.is_candidate_eligible,
        'registration_complete': bool(
            student.faculty_id and
            student.department_id and
            student.program_id and
            student.academic_year_id and
            student.semester_id
        )
    }

    # ✅ REAL AUDIT TIMELINE (ONLY THIS)
    timeline = AuditLog.query.filter_by(
        entity_type='student',
        entity_id=student.id
    ).order_by(
        AuditLog.created_at.desc()
    ).limit(20).all()

    return render_template(
        'admin/students/profile.html',
        student=student,
        profile_stats=profile_stats,
        timeline=timeline
    )
# ==========================================
# Dynamic Academic APIs
# ==========================================

@main.route('/api/departments/<int:faculty_id>')
@login_required
def api_departments(faculty_id):

    departments = Department.query.filter_by(
        faculty_id=faculty_id,
        is_active=True
    ).order_by(Department.name).all()

    data = [
        {
            'id': d.id,
            'name': d.name,
            'code': d.code
        }
        for d in departments
    ]

    return jsonify(data)


@main.route('/api/programs/<int:department_id>')
@login_required
def api_programs(department_id):

    programs = Program.query.filter_by(
        department_id=department_id,
        is_active=True
    ).order_by(Program.name).all()

    data = [
        {
            'id': p.id,
            'name': p.name,
            'code': p.code
        }
        for p in programs
    ]

    return jsonify(data)


@main.route('/api/semesters/<int:program_id>')
@login_required
def api_semesters(program_id):

    # Find program
    program = Program.query.get_or_404(program_id)

    # Get current academic year
    current_year = AcademicYear.query.filter_by(
        is_current=True
    ).first()

    if not current_year:
        return jsonify([])

    # Get semesters of current academic year
    semesters = Semester.query.filter_by(
        academic_year_id=current_year.id,
        is_active=True
    ).order_by(Semester.semester_number).all()

    data = [
        {
            'id': s.id,
            'name': s.name,
            'number': s.semester_number
        }
        for s in semesters
    ]

    return jsonify(data)
# ==========================================
# Student Verification Workflow
# ==========================================
@main.route('/admin/students/verify/<int:id>')
@login_required
@super_admin_required
def verify_student(id):

    student = Student.query.get_or_404(id)

    # Verify student
    student.is_verified = True

    # 🔥 THIS IS THE AUDIT IMPLEMENTATION
    log_action(
        action='verify_student',
        entity_type='student',
        entity_id=student.id,
        description=f'Verified student {student.first_name} {student.last_name}'
    )

    # Save both student + audit log
    db.session.commit()

    flash('Student verified successfully.', 'success')

    return redirect(url_for('main.student_profile', id=id))

@main.route('/admin/students/reject/<int:id>')
@login_required
@super_admin_required
def reject_student(id):

    student = Student.query.get_or_404(id)
    student.is_verified = False

    # 🔥 AUDIT ENTRY
    log_action(
        action='reject_student',
        entity_type='student',
        entity_id=student.id,
        description=f'Rejected verification for {student.first_name} {student.last_name}'
    )

    db.session.commit()

    try:

        student.is_verified = False
        student.is_candidate_eligible = False

        db.session.commit()

        flash(
            f'{student.full_name} verification has been rejected.',
            'warning'
        )

    except Exception:

        db.session.rollback()

        flash(
            'Unable to reject verification.',
            'danger'
        )

    return redirect(
        url_for('main.student_profile', id=student.id)
    )

# ==========================================
# Student Import / Export
# ==========================================
# ==========================================
# Student Import (CSV + Excel)
# ==========================================

@main.route('/admin/students/import', methods=['GET', 'POST'])
@login_required
@super_admin_required
def import_students():

    result = None

    # --------------------------
    # POST: Handle file upload
    # --------------------------
    if request.method == 'POST':

        file = request.files.get('file')

        # No file selected
        if not file or file.filename == '':

            flash(
                'Please select a CSV or Excel file.',
                'warning'
            )

            return redirect(request.url)

        filename = file.filename.lower()

        # Allowed extensions
        allowed = ('.csv', '.xlsx', '.xls')

        if not filename.endswith(allowed):

            flash(
                'Only .csv and .xlsx files are allowed.',
                'danger'
            )

            return redirect(request.url)

        try:

            # Temporary file path
            temp_path = f'temp_{filename}'

            # Save uploaded file
            file.save(temp_path)

            # Import students
            result = import_students_file(temp_path)

            # Delete temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            # Flash messages
            if result['success'] > 0:

                flash(
                    f'{result["success"]} students imported successfully.',
                    'success'
                )

            if result['failed'] > 0:

                flash(
                    f'{result["failed"]} rows failed validation.',
                    'warning'
                )

        except Exception as e:

            flash(
                f'Import failed: {str(e)}',
                'danger'
            )

    # --------------------------
    # GET + POST final response
    # --------------------------
    return render_template(
        'admin/students/import.html',
        result=result
    )
@main.route('/admin/students/export')
@login_required
@super_admin_required
def export_students():

    import csv
    from io import StringIO
    from flask import make_response, request

    # Base query
    query = Student.query

    # Filters
    search = request.args.get('search', '').strip()
    faculty_id = request.args.get('faculty', '')
    verified = request.args.get('verified', '')
    status = request.args.get('status', '')

    # Search
    if search:
        query = query.filter(
            db.or_(
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%'),
                Student.email.ilike(f'%{search}%'),
                Student.student_id.ilike(f'%{search}%')
            )
        )

    # Faculty filter
    if faculty_id:
        query = query.filter(Student.faculty_id == int(faculty_id))

    # Verification filter
    if verified == 'verified':
        query = query.filter(Student.is_verified == True)

    elif verified == 'unverified':
        query = query.filter(Student.is_verified == False)

    # Status filter
    if status == 'active':
        query = query.filter(Student.is_active == True)

    elif status == 'inactive':
        query = query.filter(Student.is_active == False)

    # Get filtered students
    students = query.order_by(Student.created_at.desc()).all()

    # Create CSV in memory
    output = StringIO()

    writer = csv.writer(output)

    # Header
    writer.writerow([
        'Student ID',
        'First Name',
        'Last Name',
        'Email',
        'Phone',
        'Faculty',
        'Department',
        'Program',
        'Academic Year',
        'Semester',
        'Verified',
        'Active'
    ])

    # Data rows
    for student in students:

        writer.writerow([
            student.student_id,
            student.first_name,
            student.last_name,
            student.email,
            student.phone,
            student.faculty.name if student.faculty else '',
            student.department.name if student.department else '',
            student.program.name if student.program else '',
            student.academic_year.name if student.academic_year else '',
            student.semester.name if student.semester else '',
            'Yes' if student.is_verified else 'No',
            'Yes' if student.is_active else 'No'
        ])

    # Build response
    response = make_response(output.getvalue())

    response.headers['Content-Disposition'] = 'attachment; filename=students_export.csv'
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'

    return response
# ==========================================
# CSV Template Download
# ==========================================

@main.route('/admin/students/template/csv')
@login_required
@super_admin_required
def download_student_csv_template():

    csv_content = '''first_name,last_name,gender,date_of_birth,email,phone,faculty,department,program,academic_year,semester,admission_year
Rahmat,Husain,Male,2004-05-12,rahmat@example.com,9800000000,Science,Information Technology,BIT,2026/27,First Semester,2026
'''

    output = StringIO()
    output.write(csv_content)
    output.seek(0)

    return send_file(
        BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='student_import_template.csv'
    )
@main.route("/admin/elections")
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def manage_elections():

    search = request.args.get("search", "").strip()

    status = request.args.get("status", "")

    election_type = request.args.get("type", "")

    page = request.args.get("page", 1, type=int)

    show_archived = request.args.get("archived")

    query = Election.query

    if not show_archived:
        query = query.filter_by(is_active=True)

    # Search

    if search:
        query = query.filter(
            Election.title.ilike(f"%{search}%")
        )

    # Status Filter

    if status:
        query = query.filter(
            Election.status == status
        )

    # Election Type

    if election_type:
        query = query.filter(
            Election.election_type == election_type
        )

    elections = query.order_by(
        Election.created_at.desc()
    ).paginate(
        page=page,
        per_page=10
    )
    stats = {
    "total": Election.query.count(),
    "active": Election.query.filter_by(is_active=True).count(),
    "archived": Election.query.filter_by(is_active=False).count(),
    "running": Election.query.filter_by(status="active").count(),
    "completed": Election.query.filter_by(status="completed").count(),
    }

    return render_template(
        "admin/elections/manage.html",
        elections=elections,
        stats=stats,
        search=search,
        status=status,
        election_type=election_type
    )
@main.route("/admin/elections/create", methods=["GET", "POST"])
@login_required
@super_admin_required
def create_election():

    form = ElectionForm()

    if form.validate_on_submit():

        election = Election(
            title=form.title.data,
            academic_year=form.academic_year.data,

            election_type=form.election_type.data,
            description=form.description.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data,
            status=form.status.data,
            created_by=current_user.id
            )

        db.session.add(election)
        db.session.commit()

        # Audit Log
        log = AuditLog(
            user_id=current_user.id,
            action="create_election",
            entity_type="election",
            entity_id=election.id,
            description=f"Created election '{election.title}'"
        )

        db.session.add(log)
        db.session.commit()

        flash("Election created successfully!", "success")

        return redirect(url_for("main.manage_elections"))

    return render_template(
        "admin/elections/create.html",
            form=form
    )
@main.route("/admin/elections/<int:election_id>/delete", methods=["POST"])
@login_required
@super_admin_required
def delete_election(election_id):
    """
    Soft Delete Election
    """

    election = Election.query.filter_by(
        id=election_id,
        is_active=True
    ).first_or_404()

    # Prevent deleting active elections
    if election.status == "active":
        flash(
            "Active elections cannot be deleted. Complete the election first.",
            "danger"
        )
        return redirect(url_for("main.manage_elections"))

    try:
        # Soft Delete
        election.is_active = False

        db.session.commit()

        # Audit Log
        log = AuditLog(
            user_id=current_user.id,
            action="delete_election",
            entity_type="election",
            entity_id=election.id,
            description=f"Deleted election '{election.title}'"
        )

        db.session.add(log)
        db.session.commit()

        flash(
            "Election deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            "Failed to delete election.",
            "danger"
        )

        current_app.logger.error(e)

    return redirect(url_for("main.manage_elections"))

@main.route("/admin/elections/<int:election_id>/archive", methods=["POST"])
@login_required
@super_admin_required
def archive_election(election_id):

    election = Election.query.get_or_404(election_id)

    election.is_active = False

    db.session.commit()

    log_action(
        user=current_user,
        action="Archive Election",
        description=f"Archived election '{election.title}'"
    )

    flash(
        "Election archived successfully.",
        "warning"
    )

    return redirect(
        url_for("main.manage_elections")
    )

@main.route("/admin/elections/<int:election_id>/edit",
            methods=["GET", "POST"])
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def edit_election(election_id):

    election = Election.query.get_or_404(election_id)

    form = ElectionForm(obj=election)

    if form.validate_on_submit():

        election.title = form.title.data
        election.academic_year = form.academic_year.data
        election.election_type = form.election_type.data
        election.description = form.description.data
        election.start_datetime = form.start_datetime.data
        election.end_datetime = form.end_datetime.data
        election.status = form.status.data

        db.session.commit()

        log_action(
            action="Election Updated",
            entity_type="Election",
            entity_id=election.id,
            description=f"Updated election '{election.title}'"
        )

        flash(
            "Election updated successfully.",
            "success"
        )

        return redirect(
            url_for("main.manage_elections")
        )

    return render_template(
        "admin/elections/edit.html",
        form=form,
        election=election
    )

@main.route("/admin/elections/<int:election_id>")
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def election_detail(election_id):

    election = Election.query.get_or_404(election_id)

    positions = Position.query.filter(
        Position.election_id == election.id
    ).order_by(
        Position.display_order
    ).all()

    return render_template(
        "admin/elections/detail.html",
        election=election,
        positions=positions
    )

@main.route("/admin/elections/<int:election_id>/positions")
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def manage_positions(election_id):

    election = Election.query.get_or_404(election_id)

    search = request.args.get("search", "").strip()

    status = request.args.get("status", "")

    page = request.args.get("page", 1, type=int)

    query = Position.query.filter_by(
        election_id=election.id
    )

    if search:
        query = query.filter(
            Position.title.ilike(f"%{search}%")
        )

    if status:
        query = query.filter(
            Position.status == status
        )

    positions = query.order_by(
        Position.display_order.asc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    stats = {
    "total": Position.query.filter_by(
        election_id=election.id
        ).count(),

    "active": Position.query.filter_by(
        election_id=election.id,
        status="active"
        ).count(),

    "archived": Position.query.filter_by(
        election_id=election.id,
        status="archived"
        ).count(),

    "filled": sum(
        1
        for p in Position.query.filter_by(
            election_id=election.id
        ).all()
        if p.is_filled
        ),

    "empty": sum(
        1
        for p in Position.query.filter_by(
            election_id=election.id
        ).all()
        if p.candidate_count == 0
        ),

    "candidates": sum(
        p.candidate_count
        for p in Position.query.filter_by(
            election_id=election.id
        ).all()
        )
        }
    return render_template(
    "admin/positions/manage.html",
    election=election,
    positions=positions,
    stats=stats,
    search=search,
    status=status
    )

@main.route(
    "/admin/elections/<int:election_id>/positions/create",
    methods=["GET", "POST"]
)
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def create_position(election_id):

    election = Election.query.get_or_404(election_id)

    form = PositionForm()

    # Populate Election dropdown
    form.election_id.choices = [
        (election.id, election.title)
    ]
    form.election_id.data = election.id

    if form.validate_on_submit():

        try:

            position = PositionService.create_position(form)

            log = AuditLog(
                user_id=current_user.id,
                action="create_position",
                entity_type="position",
                entity_id=position.id,
                description=f"Created position '{position.title}' for election '{election.title}'."
            )

            db.session.add(log)
            db.session.commit()

            



            flash(
                "Position created successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "main.manage_positions",
                    election_id=election.id
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Unable to create position. {str(e)}",
                "danger"
            )

    return render_template(
        "admin/positions/create.html",
        form=form,
        election=election
    )

@main.route(
    "/admin/positions/<int:position_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def edit_position(position_id):

    position = Position.query.get_or_404(position_id)

    form = PositionForm(
    original_position_id=position.id,
    obj=position
    )

    # Election should not change
    form.election_id.choices = [
        (position.election.id, position.election.title)
    ]
    form.election_id.data = position.election_id

    if form.validate_on_submit():

        duplicate = Position.query.filter(
            Position.election_id == position.election_id,
            Position.title == form.title.data.strip(),
            Position.id != position.id
        ).first()

        if duplicate:
            flash(
                "A position with this title already exists.",
                "danger"
            )
            return render_template(
                "admin/positions/edit.html",
                form=form,
                position=position,
                election=position.election
            )

        try:

            position.title = form.title.data.strip()
            position.description = form.description.data
            position.max_candidates = form.max_candidates.data
            position.max_votes = form.max_votes.data
            position.display_order = form.display_order.data
            position.status = form.status.data

            audit = AuditLog(
                user_id=current_user.id,
                action="edit_position",
                entity_type="position",
                entity_id=position.id,
                description=f"Updated position '{position.title}'"
            )

            db.session.add(audit)

            db.session.commit()

            flash(
                "Position updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "main.manage_positions",
                    election_id=position.election_id
                )
            )

        except Exception:

            db.session.rollback()

            flash(
                "Unable to update position.",
                "danger"
            )

    return render_template(
        "admin/positions/edit.html",
        form=form,
        position=position,
        election=position.election
    )

@main.route(
    "/admin/positions/<int:position_id>/archive",
    methods=["POST", "GET"]
)
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def archive_position(position_id):

    position = Position.query.get_or_404(position_id)

    try:

        position.status = "archived"
        position.is_active = False

        audit = AuditLog(
            user_id=current_user.id,
            action="archive_position",
            entity_type="position",
            entity_id=position.id,
            description=f"Archived position '{position.title}'"
        )

        db.session.add(audit)

        db.session.commit()

        

        flash(
            "Position archived successfully.",
            "success"
        )

    except Exception:

        db.session.rollback()

        flash(
            "Unable to archive position.",
            "danger"
        )

    return redirect(
        url_for(
            "main.manage_positions",
            election_id=position.election_id
        )
    )

@main.route(
    "/admin/positions/<int:position_id>/candidates/create",
    methods=["GET", "POST"]
)
@login_required
@role_required(User.SUPER_ADMIN, User.ELECTION_OFFICER)
def create_candidate(position_id):

    position = Position.query.get_or_404(position_id)

    form = CandidateForm()

    # Load students as dropdown
    students = Student.query.order_by(Student.first_name).all()

    form.student_id.choices = [
        (s.id, f"{s.student_id} - {s.first_name} {s.last_name}")
        for s in students
    ]

    if form.validate_on_submit():

        # Prevent duplicate student in same position
        duplicate = Candidate.query.filter_by(
            position_id=position.id,
            student_id=form.student_id.data
        ).first()

        if duplicate:
            flash(
                "Student is already a candidate for this position.",
                "danger"
            )
            return render_template(
                "admin/candidates/create.html",
                form=form,
                position=position
            )

        candidate = Candidate(
            position_id=position.id,
            student_id=form.student_id.data,
            slogan=form.slogan.data,
            manifesto=form.manifesto.data,
            symbol=form.symbol.data,
            status=form.status.data
        )

        db.session.add(candidate)

        log_action(
            action="Create Candidate",
            entity_type="Candidate",
            entity_id=0,
            description=f"Candidate added to {position.title}"
        )

        db.session.commit()

        flash(
            "Candidate created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "main.manage_candidates",
                position_id=position.id
            )
        )

    return render_template(
        "admin/candidates/create.html",
        form=form,
        position=position
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
   