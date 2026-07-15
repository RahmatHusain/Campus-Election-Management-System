from datetime import datetime

from app import db


class Program(db.Model):
    __tablename__ = "programs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    code = db.Column(
        db.String(20),
        nullable=False
    )

    duration_years = db.Column(
        db.Integer,
        nullable=False,
        default=4
    )

    total_semesters = db.Column(
        db.Integer,
        nullable=False,
        default=8
    )

    description = db.Column(
        db.Text
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

    department = db.relationship(
        "Department",
        backref=db.backref(
            "programs",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    __table_args__ = (

        db.UniqueConstraint(
            "department_id",
            "name",
            name="uq_program_name_department"
        ),

        db.UniqueConstraint(
            "department_id",
            "code",
            name="uq_program_code_department"
        ),

    )

    def __repr__(self):
        return f"<Program {self.name}>"