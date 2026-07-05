from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user, login_required

from app.models.user import User
from flask import abort

def role_required(*roles):
    """
    Generic Role Decorator

    Example:
    @role_required(User.SUPER_ADMIN)
    """

    def decorator(view):

        @wraps(view)
        @login_required
        def wrapped_view(*args, **kwargs):

            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped_view

    return decorator


def super_admin_required(view):
    return role_required(User.SUPER_ADMIN)(view)


def election_officer_required(view):
    return role_required(User.ELECTION_OFFICER)(view)


def student_required(view):
    return role_required(User.STUDENT)(view)