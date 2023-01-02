import os

from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

from database.db import db
from database.models.user import UserProfile

from utils.email import mail
from utils.config import database_config, email_config
from utils.models.auth_manager import create_admin


def create_app():
    migrate = Migrate()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_config()

    # Initialize Bootstrap5
    bootstrap = Bootstrap5(app)

    # Initialize database and flask-migration
    db.init_app(app)
    migrate.init_app(app, db, directory='database/migrations')

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app=app)

    # Initialize Flask-mail
    email_config(app)
    mail.init_app(app)

    # define the app context
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'mail': mail}

    @login_manager.user_loader
    def load_user(user_id):
        # TODO change with the value
        return UserProfile.query.get(int(user_id))

    return app
