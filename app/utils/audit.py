from flask import request
from flask_login import current_user

from app import db
from app.models.audit_log import AuditLog


def log_action(
    action,
    entity_type,
    entity_id,
    description
):

    try:

        log = AuditLog(
            user_id=current_user.id
            if current_user.is_authenticated
            else None,

            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            ip_address=request.remote_addr
        )

        db.session.add(log)

    except Exception:
        # Never break the main request
        pass