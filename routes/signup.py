from flask import Blueprint, render_template, abort
from flask_login import login_user, current_user
from utils.user import UserModel
from jinja2 import TemplateNotFound
from utils.form import RegisterForm
from utils.constats import year, SITE_NAME

signup_route = Blueprint('signup', __name__, template_folder="routes")


@signup_route.route('/register', methods=["GET", "POST"])
def register():
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            data = {
                "user_id": "",
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data
            }
            user = UserModel(data).register_user()
            print(user)
            if user:
                login_user(user)
                return render_template('index.html', year=year, current_user=current_user)
        return render_template('sign_up.html', name=SITE_NAME, form=form, year=year, current_user=current_user)
    except TemplateNotFound:
        abort(404)
