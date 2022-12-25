from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from datetime import datetime
from utils.forms import DateTimeForm_start, DateTimeForm_finish

from database.db import db
from database.models.schedule_datetime import ScheduleDatetime

scheduling_datetime_route = Blueprint('scheduling_datetime', __name__, template_folder="routes")


@scheduling_datetime_route.route('/scheduling_datetime', methods=['GET', 'POST'])
def scheduling_datetime():
    dtf_start = DateTimeForm_start()
    dtf_finish = DateTimeForm_finish()
    
    if request.method == 'POST':
        try:
            if current_user.is_authenticated:
                #to make a schedule
                if dtf_start.validate_on_submit() and dtf_finish.validate_on_submit():
                    dt_start_val= request.form['dt_start']
                    dt_finish_val = request.form['dt_finish']

                    #validate two inputs
                    first = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
                    second = datetime.strptime(dt_finish_val, "%Y/%m/%d %H:%M")
                    if ( second - first ).total_seconds() < 0 :
                        return render_template('scheduling_datetime.html', year=YEAR, 
                        form_start=dtf_start, form_finish=dtf_finish, message="Validation error")
                    try:
                        #insert data into db
                        opening_slot = ScheduleDatetime(start_at = dt_start_val, finish_at = dt_finish_val, user_opening_slot = current_user.id)
                        db.session.add(opening_slot)
                        db.session.commit()
                        ## todo: initialize input 
                        return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, 
                        form_start=dtf_start, form_finish=dtf_finish, 
                        date_start=dt_start_val, date_finish=dt_finish_val, message="Success")
                    except TemplateNotFound: return abort(404)
                return render_template('scheduling_datetime.html', year=YEAR, 
                form_start=dtf_start, form_finish=dtf_finish, message="Validation error")
        except TemplateNotFound: return abort(404)
    else:
        try:
            if current_user.is_authenticated:
                return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, form_start=dtf_start, form_finish=dtf_finish)
            return render_template('scheduling_datetime.html', year=YEAR, form_start=dtf_start, form_finish=dtf_finish)
        except TemplateNotFound: return abort(404)
