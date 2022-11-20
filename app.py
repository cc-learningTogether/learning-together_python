import os

from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5

from database.db import db

from alembic import op

DATABASE_URL = os.getenv('URL')
DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PW = os.getenv('POSTGRES_PW')
DATABASE_DB = os.getenv('POSTGRES_DB')
POSTGRES_URL = os.getenv('POSTGRES_URL')

if POSTGRES_URL:
    DB_URL = POSTGRES_URL
else:
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=DATABASE_USER, pw=DATABASE_PW, url=DATABASE_URL,
                                                                   db=DATABASE_DB)


def create_app():
    migrate = Migrate()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

    # Initialize Bootstrap5
    bootstrap = Bootstrap5(app)

    # Initialize database and flask-migration
    db.init_app(app)
    migrate.init_app(app, db, directory='database/migrations')

    return app

