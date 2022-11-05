from flask import Flask, render_template
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from utils.form import LoginForm, RegisterForm
from datetime import datetime
from flask_login import LoginManager, current_user, login_user, logout_user
from app import create_app
from test_data_folder.user_data import users
from utils.user import User

import os

app = create_app()

SITE_NAME = "Learning Together"

year = datetime.now().year


@app.route('/')
def home():
    return render_template('index.html', year=year)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.email.data)
    return render_template('sign_up.html', name=SITE_NAME, form=form, year=year)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.login_email.data
        # TODO change this part with the database model for the user.py
        #  (user1 = the value you get from the database after the input check)
        # -------- test data --------
        user = [user for user in users if user["email"] == email][0]
        user1 = User(user)  # this class can be used for the input check or can be deleted
        # -------------------------
        login_user(user1)
    return render_template('sign_in.html', name=SITE_NAME, form=form, year=year)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
