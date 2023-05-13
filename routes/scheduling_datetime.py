from flask import Blueprint, render_template, abort, request, redirect
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
    if dtf.validate_on_submit():  # if request.method is POST
        dt_start_val = request.form['dt_start']
        dt_finish_val = request.form['dt_finish']
        if dt_finish_val == '':  # Check input of 'Finish at'
            return render_template('scheduling_datetime.html', year=YEAR,
                                   dtf_form=dtf, message="*'Finish at' is empty")
        # Check two inputs:WTForm validation is valid only by field
        first = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
        second = datetime.strptime(dt_finish_val, "%Y/%m/%d %H:%M")
        if (second - first).total_seconds() < 0:
            return render_template('scheduling_datetime.html', year=YEAR,
                                   dtf_form=dtf, message="*'Start at' should earlier than 'Finish at'")
        try:
            opening_slot = ScheduleDatetime(start_at=dt_start_val, finish_at=dt_finish_val,
                                            user_opening_slot=current_user.id)
            db.session.add(opening_slot)
            db.session.commit()
            return redirect("/#scheduled")
        except TemplateNotFound:
            return abort(404)
    else:
        try:
            return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME,
                                   dtf_form=dtf, message=dtf  # validation error message of the date
                                   )
        except TemplateNotFound:
            return abort(404)
