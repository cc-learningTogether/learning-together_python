from flask import Flask
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from test_data_folder.user_data import users
from database.db import db
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

    app = Flask(__name__)
    # set Secret key (required from wtForms
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # add bootstrap version 5 to the application
    bootstrap = Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(user_id):
        user = [user for user in users if user["user_id"] == int(user_id)]
        return user[0]

    return app
