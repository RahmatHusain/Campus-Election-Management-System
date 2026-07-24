from datetime import datetime
from app import db


class Election(db.Model):
    __tablename__ = 'elections'

    id = db.Column(db.Integer, primary_key=True)

    # Basic Information
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Election Type
    election_type = db.Column(
        db.String(50),
        default='general'
    )

    # Schedule
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)

    # Status
    status = db.Column(
        db.String(20),
        default='upcoming'
    )

    is_published = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # Audit
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
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

    # Relationships
    creator = db.relationship(
        'User',
        backref='created_elections'
    )

    # Helper Properties
    @property
    def is_upcoming(self):
        return self.status == 'upcoming'

    @property
    def is_running(self):
        return self.status == 'active'

    @property
    def is_completed(self):
        return self.status == 'completed'

    def __repr__(self):
        return f'<Election {self.title}>'