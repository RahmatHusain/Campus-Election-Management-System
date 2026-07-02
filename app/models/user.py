from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

# ==========================
# User Role Constants
# ==========================

ROLE_SUPER_ADMIN = "SUPER_ADMIN"
ROLE_ELECTION_OFFICER = "ELECTION_OFFICER"
ROLE_STUDENT = "STUDENT"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    student_id = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
    db.String(30),
    nullable=False,
    default=ROLE_STUDENT
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Login Tracking
    last_login = db.Column(db.DateTime, nullable=True)

    last_logout = db.Column(db.DateTime, nullable=True)

    login_count = db.Column(db.Integer, default=0)

    # Account Status
    is_active_user = db.Column(db.Boolean, default=True)

    # Security
    failed_login_attempts = db.Column(db.Integer, default=0)

    account_locked_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
       
    # ==========================
    # Role Helper Methods
    # ==========================

    def is_super_admin(self):
        return self.role == ROLE_SUPER_ADMIN

    def is_election_officer(self):
        return self.role == ROLE_ELECTION_OFFICER

    def is_student(self):
        return self.role == ROLE_STUDENT
    
    def __repr__(self):
        return f"<User {self.email}>"