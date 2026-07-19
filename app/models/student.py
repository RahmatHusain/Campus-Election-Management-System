from datetime import datetime

from app import db


class Student(db.Model):
    __tablename__ = "students"

    # ==========================
    # Primary Information
    # ==========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    gender = db.Column(
        db.String(20),
        nullable=False
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    # ==========================
    # Contact Information
    # ==========================

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    address = db.Column(
        db.Text
    )

    # ==========================
    # Academic Relationships
    # ==========================

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculties.id"),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    program_id = db.Column(
        db.Integer,
        db.ForeignKey("programs.id"),
        nullable=False
    )

    academic_year_id = db.Column(
        db.Integer,
        db.ForeignKey("academic_years.id"),
        nullable=False
    )

    semester_id = db.Column(
        db.Integer,
        db.ForeignKey("semesters.id"),
        nullable=False
    )

    # ==========================
    # Admission Information
    # ==========================

    admission_year = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    roll_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True
    )

    batch = db.Column(
        db.String(20)
    )

    # ==========================
    # Profile
    # ==========================

    photo = db.Column(
        db.String(255)
    )

    # ==========================
    # Election Eligibility
    # ==========================

    is_voter = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    is_candidate_eligible = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # ==========================
    # System
    # ==========================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ==========================
    # Relationships
    # ==========================

    faculty = db.relationship(
        "Faculty",
        backref=db.backref(
            "students",
            lazy=True
        )
    )

    department = db.relationship(
        "Department",
        backref=db.backref(
            "students",
            lazy=True
        )
    )

    program = db.relationship(
        "Program",
        backref=db.backref(
            "students",
            lazy=True
        )
    )

    academic_year = db.relationship(
        "AcademicYear",
        backref=db.backref(
            "students",
            lazy=True
        )
    )

    semester = db.relationship(
        "Semester",
        backref=db.backref(
            "students",
            lazy=True
        )
    )

    # ==========================
    # Helper Properties
    # ==========================

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def election_status(self):
        if not self.is_active:
            return "Inactive"

        if not self.is_verified:
            return "Pending Verification"

        if self.is_candidate_eligible:
            return "Eligible Candidate"

        if self.is_voter:
            return "Eligible Voter"

        return "Not Eligible"

    # ==========================
    # Representation
    # ==========================

    def __repr__(self):
        return f"<Student {self.student_id} - {self.full_name}>"