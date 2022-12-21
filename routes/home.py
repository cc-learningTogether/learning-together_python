from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from flask_wtf import FlaskForm
from wtforms.fields import DateTimeField

home_route = Blueprint('home', __name__, template_folder="routes")


class DateTimeForm_start(FlaskForm):
    dt_start = DateTimeField()
class DateTimeForm_finish(FlaskForm):
    dt_finish = DateTimeField()


@home_route.route('/', methods=['GET', 'POST'])
def home():
    dtf_start = DateTimeForm_start()
    dtf_finish = DateTimeForm_finish()

    if request.method == 'POST':
        dt_start_val= request.form['dt_start']
        dt_finish_val = request.form['dt_finish']
        dt_start_val_type = type(dt_start_val)
        try:
            if current_user.is_authenticated:
                return render_template('index.html', year=YEAR, name=SITE_NAME, 
                form_start=dtf_start, form_finish=dtf_finish, 
                date_start=dt_start_val, date_finish=dt_finish_val, date_start_type=dt_start_val_type)

            return render_template('index.html', year=YEAR, form_start=dtf_start, form_finish=dtf_finish)
        except TemplateNotFound:
            return abort(404)

    else:
        try:
            if current_user.is_authenticated:
                return render_template('index.html', year=YEAR, name=SITE_NAME, form_start=dtf_start, form_finish=dtf_finish)
            return render_template('index.html', year=YEAR, form_start=dtf_start, form_finish=dtf_finish)
        except TemplateNotFound:
            return abort(404)
