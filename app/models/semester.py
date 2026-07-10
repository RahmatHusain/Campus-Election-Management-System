from datetime import datetime

from app import db


class Semester(db.Model):
    __tablename__ = "semesters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    academic_year_id = db.Column(
        db.Integer,
        db.ForeignKey("academic_years.id"),
        nullable=False
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    semester_number = db.Column(
        db.Integer,
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    is_current = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    academic_year = db.relationship(
        "AcademicYear",
        backref=db.backref(
            "semesters",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    __table_args__ = (

        db.UniqueConstraint(
            "academic_year_id",
            "semester_number",
            name="uq_semester_number_per_year"
        ),

        db.UniqueConstraint(
            "academic_year_id",
            "name",
            name="uq_semester_name_per_year"
        ),
    )

    def __repr__(self):
        return f"<Semester {self.name}>"