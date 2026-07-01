from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from pathlib import Path

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Debug information
    print("SECRET_KEY:", app.config["SECRET_KEY"])
    print("DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Project Root:", Path.cwd())

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main
    app.register_blueprint(main)
    
    return app 
