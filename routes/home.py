from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
from datetime import datetime

from database.db import db
from database.models.schedule_datetime import ScheduleDatetime


home_route = Blueprint('home', __name__, template_folder="routes")


class DateTimeForm_start(FlaskForm):
    dt_start = StringField("datetime_start", validators=[DataRequired()])

    def validate_dt_start(self, dt_start):
        # incorrect input 
        date = datetime.strptime(dt_start.data, "%Y/%m/%d %H:%M")
        if ( date - datetime.now() ).total_seconds() < 0 :
            raise ValidationError("Chose later than today")


class DateTimeForm_finish(FlaskForm):
    dt_finish = StringField("datetime_finish", validators=[DataRequired()])

    def validate_dt_finish(self, dt_finish):
        # incorrect input 
        date = datetime.strptime(dt_finish.data, "%Y/%m/%d %H:%M")
        if ( date - datetime.now() ).total_seconds() < 0 :
            raise ValidationError("Chose later than today")


@home_route.route('/', methods=['GET', 'POST'])
def home():
    dtf_start = DateTimeForm_start()
    dtf_finish = DateTimeForm_finish()
    
    #query all user's slots 
    open_slot = ScheduleDatetime.query.filter_by(user_opening_slot=current_user.id).all()


    if request.method == 'POST':
        if dtf_start.validate_on_submit() and dtf_finish.validate_on_submit():
            dt_start_val= request.form['dt_start']
            dt_finish_val = request.form['dt_finish']

            #validate two inputs
            first = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
            second = datetime.strptime(dt_finish_val, "%Y/%m/%d %H:%M")
            if ( second - first ).total_seconds() < 0 :
                return render_template('index.html', year=YEAR, 
                form_start=dtf_start, form_finish=dtf_finish, message="Validation error")

            try:
                if current_user.is_authenticated:
                    #insert data into db
                    opening_slot = ScheduleDatetime(start_at = dt_start_val, finish_at = dt_finish_val, user_opening_slot = current_user.id)
                    db.session.add(opening_slot)
                    db.session.commit()
                    ## todo: initialize datepicker
                    return render_template('index.html', year=YEAR, name=SITE_NAME, 
                    form_start=dtf_start, form_finish=dtf_finish, 
                    date_start=dt_start_val, date_finish=dt_finish_val, message="Success", op_slot=open_slot)
            except TemplateNotFound: return abort(404)

        return render_template('index.html', year=YEAR, 
        form_start=dtf_start, form_finish=dtf_finish, message="Validation error")

    else:
        try:
            if current_user.is_authenticated:

                return render_template('index.html', year=YEAR, name=SITE_NAME, form_start=dtf_start, form_finish=dtf_finish, op_slot=open_slot)
            return render_template('index.html', year=YEAR, form_start=dtf_start, form_finish=dtf_finish)
        except TemplateNotFound: return abort(404)
