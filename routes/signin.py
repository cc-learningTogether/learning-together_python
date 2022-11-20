from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils.forms import LoginForm
from utils.constants import YEAR, SITE_NAME
from utils.helper import user_login
import uuid

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
            response = user_login(data)
            if response['user']:
                # TODO add login stuff here
                return render_template("index.html", year=YEAR)
            if response['errors']:
                print(type(str(response['errors'])))
                return render_template('sign_in.html', name=SITE_NAME, form=form, year=YEAR,
                                       errors=str(response['errors']))
            return render_template('index.html', year=YEAR, errors='')
        return render_template('sign_in.html', name=SITE_NAME, form=form, year=YEAR, errors='')
    except TemplateNotFound:
        return abort(404)
