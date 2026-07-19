from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    DateField,
    SelectField,
    BooleanField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError
)

from app.models.faculty import Faculty
from app.models.department import Department
from app.models.program import Program
from app.models.academic_year import AcademicYear
from app.models.semester import Semester
from app.models.student import Student


class StudentForm(FlaskForm):

    # ==========================
    # Personal Information
    # ==========================

    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ],
        validators=[DataRequired()]
    )

    date_of_birth = DateField(
        "Date of Birth",
        validators=[DataRequired()]
    )

    # ==========================
    # Contact Information
    # ==========================

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=7, max=20)
        ]
    )

    address = TextAreaField(
        "Address",
        validators=[Length(max=500)]
    )

    # ==========================
    # Academic Information
    # ==========================

    faculty_id = SelectField(
        "Faculty",
        coerce=int,
        validators=[DataRequired()]
    )

    department_id = SelectField(
        "Department",
        coerce=int,
        validators=[DataRequired()]
    )

    program_id = SelectField(
        "Program",
        coerce=int,
        validators=[DataRequired()]
    )

    academic_year_id = SelectField(
        "Academic Year",
        coerce=int,
        validators=[DataRequired()]
    )

    semester_id = SelectField(
        "Semester",
        coerce=int,
        validators=[DataRequired()]
    )

    admission_year = SelectField(
        "Admission Year",
        coerce=int,
        validators=[DataRequired()]
    )

    batch = StringField(
        "Batch",
        validators=[Length(max=20)]
    )

    # ==========================
    # Profile Photo
    # ==========================

    photo = FileField(
        "Profile Photo",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    # ==========================
    # Election Settings
    # ==========================

    is_voter = BooleanField(
        "Eligible to Vote",
        default=True
    )

    is_candidate_eligible = BooleanField(
        "Eligible for Candidacy",
        default=False
    )

    is_verified = BooleanField(
        "Verified by Administration",
        default=False
    )

    is_active = BooleanField(
        "Active Student",
        default=True
    )

    submit = SubmitField("Save Student")

    # ==========================
    # Dynamic Dropdowns
    # ==========================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.faculty_id.choices = [
            (f.id, f.name)
            for f in Faculty.query.filter_by(
                is_active=True
            ).order_by(Faculty.name).all()
        ]

        self.department_id.choices = [
            (d.id, d.name)
            for d in Department.query.filter_by(
                is_active=True
            ).order_by(Department.name).all()
        ]

        self.program_id.choices = [
            (p.id, f"{p.name} ({p.code})")
            for p in Program.query.filter_by(
                is_active=True
            ).order_by(Program.name).all()
        ]

        self.academic_year_id.choices = [
            (a.id, a.name)
            for a in AcademicYear.query.filter_by(
                is_active=True
            ).order_by(AcademicYear.start_date.desc()).all()
        ]

        self.semester_id.choices = [
            (s.id, s.name)
            for s in Semester.query.filter_by(
                is_active=True
            ).order_by(Semester.semester_number).all()
        ]

        current_year = date.today().year

        self.admission_year.choices = [
            (year, str(year))
            for year in range(current_year - 5, current_year + 2)
        ]

    # ==========================
    # Validation
    # ==========================

    def validate_email(self, field):

        existing = Student.query.filter_by(
            email=field.data.strip().lower()
        ).first()

        if existing:
            raise ValidationError(
                "Email is already registered."
            )

    def validate_phone(self, field):

        if not field.data.isdigit():
            raise ValidationError(
                "Phone number must contain only digits."
            )

    def validate_date_of_birth(self, field):

        today = date.today()

        age = today.year - field.data.year - (
            (today.month, today.day) < (field.data.month, field.data.day)
        )

        if age < 15:
            raise ValidationError(
                "Student must be at least 15 years old."
            )

        if age > 60:
            raise ValidationError(
                "Invalid student age."
            )

    def validate_admission_year(self, field):

        current_year = date.today().year

        if field.data < 2000 or field.data > current_year + 1:
            raise ValidationError(
                "Invalid admission year."
            )