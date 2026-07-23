from app import db
from app.models.audit_log import AuditLog

def log_action(user_id, action, entity_type, entity_id=None, details=None):

    log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )

    db.session.add(log)