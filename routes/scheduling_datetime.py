from flask import Blueprint, render_template, abort, request, session, redirect
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
        if dtf.validate_on_submit():
            dt_start_val= request.form['dt_start']
            dt_finish_val = request.form['dt_finish']
            # Check input of 'Finish'
            if dt_finish_val == '': 
                return render_template('scheduling_datetime.html', year=YEAR, 
                dtf_form=dtf, message="'Finish' is empty")
            # Check two inputs:WTForm validation is valid only by field
            first = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
            second = datetime.strptime(dt_finish_val, "%Y/%m/%d %H:%M")
            if ( second - first ).total_seconds() < 0 :
                return render_template('scheduling_datetime.html', year=YEAR, 
                dtf_form=dtf, message="'Start' should earlier than 'Finish'")
            try:
                #insert data into db
                opening_slot = ScheduleDatetime(start_at = dt_start_val, finish_at = dt_finish_val, user_opening_slot = current_user.id)
                db.session.add(opening_slot)
                db.session.commit()

                ## todo: initialize input 
                # session["date_start"] = dt_start_val
                # session["date_finish"] = dt_finish_val
                # session["message"] = "Success"
                return redirect("/#scheduled")
                # return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, 
                # date_start=dt_start_val, date_finish=dt_finish_val, 
                # dtf_form=dtf, message="Success")
            except TemplateNotFound: return abort(404)
        else: 
            return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, 
            dtf_form=dtf, message="Invalid input")
    else:
        try:
            # formdata_message = session.get("message", None)
            # if formdata_message:
            #     f_message = formdata_message
            return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, dtf_form=dtf)
 
            return render_template('scheduling_datetime.html', year=YEAR, name=SITE_NAME, dtf_form=dtf)
        except TemplateNotFound: return abort(404)
