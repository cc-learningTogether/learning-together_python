from flask import Flask
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from database.db import db
from database.user import User
import os

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                               db=POSTGRES_DB)


def create_app():
    # initialize the env variable
    load_dotenv()
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PW = os.getenv("POSTGRES_PW")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                                   db=POSTGRES_DB)
    app = Flask(__name__)
    # set Secret key (required from wtForms
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # add bootstrap version 5 to the application
    bootstrap = Bootstrap5(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

    db.init_app(app=app)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    with app.app_context():
        from database.user import User
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(user_id):
        # TODO change with the value
        return User.query.get(int(user_id))

    return app
