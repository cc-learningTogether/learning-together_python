from flask import Blueprint, render_template, abort, request
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from datetime import datetime
from utils.forms import DateTimeForm

from database.db import db
from database.models.schedule_datetime import ScheduleDatetime

scheduling_datetime_route = Blueprint('scheduling_datetime', __name__, template_folder="routes")

@scheduling_datetime_route.route('/scheduling_datetime', methods=['GET', 'POST'])
@login_required
def scheduling_datetime():
    dtf = DateTimeForm()
    if request.method == 'POST':
        try:
            if dtf.validate_on_submit():
                dt_start_val= request.form['dt_start']
                dt_finish_val = request.form['dt_finish']
                #validate two inputs
                # first = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
                # second = datetime.strptime(dt_finish_val, "%Y/%m/%d %H:%M")
                # if ( second - first ).total_seconds() < 0 :
                #     return render_template('scheduling_datetime.html', year=YEAR, 
                #     form_start=dtf_start, form_finish=dtf_finish, message="Validation error")
                try:
                    #insert data into db
                    opening_slot = ScheduleDatetime(start_at = dt_start_val, finish_at = dt_finish_val, user_opening_slot = current_user.id)
                    db.session.add(opening_slot)
                    db.session.commit()
                    ## todo: initialize input 
                    return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, 
                    date_start=dt_start_val, date_finish=dt_finish_val, 
                    dtf_form=dtf, message="Success")
                except TemplateNotFound: return abort(404)
        except TemplateNotFound: return abort(404)
    else:
        try:
            return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, dtf_form=dtf)
        except TemplateNotFound: return abort(404)
