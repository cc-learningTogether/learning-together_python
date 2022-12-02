from flask import Blueprint, render_template, abort
from flask_login import login_user, current_user
from jinja2 import TemplateNotFound

from utils.forms import LoginForm
from utils.constants import YEAR, SITE_NAME
from utils.models.auth_manager import AuthManager

signin_route = Blueprint('signin', __name__, template_folder='routes')


@signin_route.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            data = {
                "email": form.login_email.data,
                "password": form.login_password.data
            }
            response = AuthManager(data).user_login()
            if response['user']:
                login_user(response['user'])
                return render_template("index.html", year=YEAR, current_user=current_user)
            if response['errors']:
                return render_template('sign_in.html', name=SITE_NAME, form=form, year=YEAR,
                                       errors=str(response['errors']), current_user=current_user)
            return render_template('index.html', year=YEAR, errors='', current_user=current_user)
        return render_template('sign_in.html', name=SITE_NAME, form=form, year=YEAR, errors='',
                               current_user=current_user)
    except TemplateNotFound:
        return abort(404)
