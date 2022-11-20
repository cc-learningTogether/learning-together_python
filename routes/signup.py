from flask import Blueprint, render_template, abort
from flask_login import login_user, current_user
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash

from utils.forms import RegisterForm
from utils.constants import YEAR, SITE_NAME
from utils.helper import register_user

signup_route = Blueprint('signup', __name__, template_folder='routes')


@signup_route.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        # TODO add the errors messages to the register form
        form = RegisterForm()
        if form.validate_on_submit():
            # TODO complete when database is ready
            if form.password.data == form.confirm_password.data:
                hashed_password = generate_password_hash(
                    form.password.data,
                    method='pbkdf2:sha256',
                    salt_length=8
                )
                data = {
                    "user_id": "",
                    "username": form.username.data,
                    "email": form.email.data,
                    "password": hashed_password,
                    "gender": form.gender.data,
                    "language": form.language.data,
                    "is_supporter": form.is_supporter.data
                }

                response = register_user(data)
                if response['user']:
                    login_user(response['user'])
                    return render_template('index.html', year=YEAR, current_user=current_user)
                if response['errors']:
                    return render_template('sign_up.html', name=SITE_NAME, form=form, year=YEAR,
                                           messages=response['errors'], current_user=current_user)
            return render_template('sign_up.html', name=SITE_NAME, form=form, year=YEAR,
                                   pass_check="Password doesn't match", messages="", current_user=current_user)
        return render_template('sign_up.html', name=SITE_NAME, form=form, year=YEAR, messages="",
                               current_user=current_user)
    except TemplateNotFound:
        return abort(404)
