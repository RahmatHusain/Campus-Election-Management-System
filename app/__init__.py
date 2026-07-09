from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from pathlib import Path



db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(minutes=30)

    print("SECRET_KEY:", app.config["SECRET_KEY"])
    print("DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Project Root:", Path.cwd())

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)

    from app.models.user import User
    app.jinja_env.globals["User"] = User

    login_manager.login_view = "main.login"
    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main
    app.register_blueprint(main)

    from flask import render_template

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    return app