from datetime import datetime

from app import db


class Position(db.Model):
    __tablename__ = "positions"

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

    # Basic Information
    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # Configuration
    max_candidates = db.Column(
        db.Integer,
        nullable=False,
        default=10
    )

    max_votes = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    display_order = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    # Status
    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # Audit Fields
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ----------------------------
    # Relationships
    # ----------------------------

    election = db.relationship(
        "Election",
        back_populates="positions"
    )

    # ----------------------------
    # Helper Properties
    # ----------------------------

    @property
    def is_archived(self):
        return self.status == "archived"

    @property
    def is_open(self):
        return self.status == "active"

    def __repr__(self):
        return (
            f"<Position {self.title}>"
        )