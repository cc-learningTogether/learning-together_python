from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from datetime import datetime
from utils.forms import RegisterForm, LoginForm, ForgotPswForm, ChangePSWForm
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# load_dotenv make possible to use a .env file for store the environment variable
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL')



#connect to database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

