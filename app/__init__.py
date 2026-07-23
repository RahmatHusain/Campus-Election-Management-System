from datetime import timedelta
from pathlib import Path

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import Config

# -------------------------------------------------
# Extensions (MUST be top-level)
# -------------------------------------------------
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


# -------------------------------------------------
# Application Factory
# -------------------------------------------------
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Session timeout
    app.permanent_session_lifetime = timedelta(minutes=30)

    # Debug info
    print('SECRET_KEY:', app.config.get('SECRET_KEY'))
    print('DATABASE URI:', app.config.get('SQLALCHEMY_DATABASE_URI'))
    print('Project Root:', Path.cwd())

    # -------------------------------------------------
    # Initialize Extensions
    # -------------------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # -------------------------------------------------
    # Login Manager
    # -------------------------------------------------
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please login to continue.'
    login_manager.login_message_category = 'warning'

    # Import User model AFTER db init
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    # Expose User class to templates
    app.jinja_env.globals['User'] = User

    # -------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------
    from app.routes import main
    app.register_blueprint(main)

    # -------------------------------------------------
    # Error Handlers
    # -------------------------------------------------
    @app.errorhandler(403)
    def forbidden(error):

        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):

        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):

        db.session.rollback()

        return render_template('errors/500.html'), 500

    return app