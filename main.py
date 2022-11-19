import os

from flask import render_template
from dotenv import load_dotenv
from datetime import datetime

from app import create_app
from utils.forms import RegisterForm, LoginForm, ForgotPswForm, ChangePSWForm

from routes.home import home_route

# load_dotenv make possible to use a .env file for store the environment variable
load_dotenv()

# create the application
app = create_app()

SITE_NAME = "Learning Together"

year = datetime.now().year

app.register_blueprint(home_route)


# @app.route('/')
# def home():
#     return render_template('index.html', year=year)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        # TODO complete when database is ready
        data = {
            "user_id": "",
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
            "gender": form.gender.data,
            "language": form.language.data,
            "is_supporter": form.is_supporter.data
        }
        print(data)
        return render_template('index.html', year=year)
    return render_template('sign_up.html', name=SITE_NAME, form=form, year=year)


@app.route('/signin', methods=["GET", "POST"])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        data = {
            form.login_email.data,
            form.login_password.data
        }
        # TODO complete when database is ready
        print(data)
        return render_template('index.html', year=year)
    return render_template('sign_in.html', name=SITE_NAME, form=form, year=year)


@app.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    form_send_email = ForgotPswForm()
    if form_send_email.validate_on_submit():
        email = form_send_email.email
        # TODO verify the presence of the email on the database and send email (Flask email or other)
        return render_template("forgot_password.html", name=SITE_NAME, form=form_send_email, year=year)
    return render_template("forgot_password.html", name=SITE_NAME, form=form_send_email, year=year)


@app.route("/change-password/<string:token>", methods=["POST", "GET"])
def change_password(token):
    # TODO verify the token
    form_change_password = ChangePSWForm()
    if form_change_password.validate_on_submit():
        # TODO check if the 2 password are the same and change the psw i the database
        # TODO decide if login directly or redirect to the login page
        pass
        return render_template('index.html', year=year)
    return render_template("change_password.html", name=SITE_NAME, form=form_send_email, year=year)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
