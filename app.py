from flask import Flask, render_template
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from utils.form import LoginForm, RegisterForm
from datetime import datetime
import os

# initialize the env variable
load_dotenv()

app = Flask(__name__)
# set Secret key (required from wtForms
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# add bootstrap version 5 to the application
bootstrap = Bootstrap5(app)
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
        print(form.login_email.data)
    return render_template('sign_in.html', name=SITE_NAME, form=form, year=year)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
