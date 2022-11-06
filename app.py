from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from datetime import datetime
from utils.forms import RegisterForm
import os

# load_dotenv make possible to use a .env file for store the environment variable
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize Bootstrap5
bootstrap = Bootstrap5(app)

SITE_NAME = "Learning Together"

year = datetime.now().year


@app.route('/')
def home():
    return render_template('index.html', year=year)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
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


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
