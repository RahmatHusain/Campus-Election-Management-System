from datetime import datetime

from app import db


class AcademicYear(db.Model):
    __tablename__ = "academic_years"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(20),
        nullable=False,
        unique=True
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

    def __repr__(self):
        return f"<AcademicYear {self.name}>"