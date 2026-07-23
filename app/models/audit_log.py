from datetime import datetime
from app import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)

    # Who performed the action
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # What happened
    action = db.Column(db.String(100), nullable=False)

    # Which entity
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)

    # Human readable message
    description = db.Column(db.Text)

    # Extra metadata
    ip_address = db.Column(db.String(45))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship
    user = db.relationship(
        'User',
        backref='audit_logs'
    )

    def __repr__(self):
        return f'<AuditLog {self.action}>'