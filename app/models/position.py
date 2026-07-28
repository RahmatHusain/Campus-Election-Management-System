from datetime import datetime

from app import db


class Position(db.Model):
    __tablename__ = "positions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    election_id = db.Column(
        db.Integer,
        db.ForeignKey("elections.id"),
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

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

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
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

    # -----------------------------------
    # Relationships
    # -----------------------------------

    election = db.relationship(
        "Election",
        back_populates="positions"
    )
    candidates = db.relationship(
        "Candidate",
        back_populates="position",
        cascade="all, delete-orphan"
    )
    # -----------------------------------
    # Helper Properties
    # -----------------------------------
    @property
    def candidate_count(self):
        return len(self.candidates)


    @property
    def is_filled(self):
        """
        Temporary until Candidate module (Day 13)
        """
        return False


    @property
    def remaining_slots(self):
        """
        Temporary until Candidate module (Day 13)
        """
        return self.max_candidates

    @property
    def progress_percentage(self):
        if self.max_candidates == 0:
            return 0

        return round(
            (self.candidate_count / self.max_candidates) * 100
        )

    @property
    def badge_color(self):

        if self.status == "archived":
            return "secondary"

        if self.is_filled:
            return "success"

        if self.candidate_count == 0:
            return "danger"

        return "primary"

    def __repr__(self):
        return f"<Position {self.title}>"