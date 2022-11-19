from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils.forms import RegisterForm
from utils.constant import YEAR, SITE_NAME

signup_route = Blueprint('signup', __name__, template_folder='routes')


@signup_route.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
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
            return render_template('index.html', year=YEAR)
        return render_template('sign_up.html', name=SITE_NAME, form=form, year=YEAR)
    except TemplateNotFound:
        return abort(404)
