from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from flask_wtf import FlaskForm
from wtforms.fields import DateField

home_route = Blueprint('home', __name__, template_folder="routes")


class DateForm(FlaskForm):
    dt = DateField('Pick a Date', format="%m/%d/%Y")


@home_route.route('/', methods=['GET', 'POST'])
def home():
    FORM = DateForm()
    if request.method == 'POST':
        ret = request.form['dt']
        ret_t = type(ret)
        try:
            if current_user.is_authenticated:
                return render_template('index.html', year=YEAR, name=SITE_NAME, form=FORM, result=ret, result_type=ret_t)

            return render_template('index.html', year=YEAR, form=FORM)
        except TemplateNotFound:
            return abort(404)

    else:
        try:
            if current_user.is_authenticated:
                return render_template('index.html', year=YEAR, name=SITE_NAME, form=FORM)
            return render_template('index.html', year=YEAR, form=FORM)
        except TemplateNotFound:
            return abort(404)
