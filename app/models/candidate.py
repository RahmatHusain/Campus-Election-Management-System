from datetime import datetime
from app import db


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Relationships
    election_id = db.Column(
        db.Integer,
        db.ForeignKey("elections.id"),
        nullable=False
    )

    position_id = db.Column(
        db.Integer,
        db.ForeignKey("positions.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    # Candidate Details
    manifesto = db.Column(
        db.Text
    )

    slogan = db.Column(
        db.String(255)
    )

    photo = db.Column(
        db.String(255)
    )

    symbol = db.Column(
        db.String(255)
    )

    vote_count = db.Column(
        db.Integer,
        default=0
    )

    display_order = db.Column(
        db.Integer,
        default=1
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )
    # pending
    # approved
    # rejected
    # withdrawn

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

    # -------------------------
    # Relationships
    # -------------------------

    election = db.relationship(
        "Election",
        back_populates="candidates"
    )

    position = db.relationship(
        "Position",
        back_populates="candidates"
    )

    student = db.relationship(
        "Student",
        back_populates="candidates"
    )

    def __repr__(self):
        return f"<Candidate {self.student_id}>"