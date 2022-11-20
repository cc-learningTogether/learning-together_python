from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils.forms import LoginForm
from utils.constants import YEAR, SITE_NAME

signin_route = Blueprint('signin', __name__, template_folder='routes')


@signin_route.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            data = {
                form.login_email.data,
                form.login_password.data
            }
            # TODO complete when database is ready
            print(data)
            return render_template('index.html', year=YEAR)
        return render_template('sign_in.html', name=SITE_NAME, form=form, year=YEAR)
    except TemplateNotFound:
        return abort(404)
