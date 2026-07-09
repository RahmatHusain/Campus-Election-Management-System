from datetime import datetime

from app import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculties.id"),
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    code = db.Column(
        db.String(20),
        nullable=False
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

    faculty = db.relationship(
        "Faculty",
        backref=db.backref(
            "departments",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    __table_args__ = (
        db.UniqueConstraint(
            "faculty_id",
            "name",
            name="uq_department_name_per_faculty"
        ),
        db.UniqueConstraint(
            "faculty_id",
            "code",
            name="uq_department_code_per_faculty"
        ),
    )

    def __repr__(self):
        return f"<Department {self.name}>"