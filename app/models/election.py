from datetime import datetime
from app import db


class Election(db.Model):
    __tablename__ = "elections"

    id = db.Column(db.Integer, primary_key=True)

    # ===========================
    # Basic Information
    # ===========================
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    academic_year = db.Column(db.String(20), nullable=False)

    election_type = db.Column(
        db.String(50),
        nullable=False,
        default="general"
    )

    # ===========================
    # Schedule
    # ===========================
    start_datetime = db.Column(
        db.DateTime,
        nullable=False
    )

    end_datetime = db.Column(
        db.DateTime,
        nullable=False
    )

    # ===========================
    # Status
    # ===========================
    status = db.Column(
        db.String(20),
        nullable=False,
        default="draft"
    )

    is_published = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # ===========================
    # Audit
    # ===========================
    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
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

    # ===========================
    # Relationships
    # ===========================
    creator = db.relationship(
        "User",
        backref="created_elections"
    )
    positions = db.relationship(
    "Position",
    back_populates="election",
    lazy=True,
    cascade="all, delete-orphan",
    order_by="Position.display_order"
    )
    candidates = db.relationship(
        "Candidate",
        back_populates="election",
        cascade="all, delete-orphan"
    )

    # ===========================
    # Helper Properties
    # ===========================
    @property
    def is_upcoming(self):
        return self.status == "scheduled"

    @property
    def is_running(self):
        return self.status == "active"

    @property
    def is_completed(self):
        return self.status == "completed"
    
    academic_year = db.Column(
    db.String(20),
    nullable=False
    )
    def __repr__(self):
        return f"<Election {self.title}>"