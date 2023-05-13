from flask import Blueprint, render_template, abort, request
from flask_login import current_user, login_required 
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from datetime import datetime

from database.db import db
from database.models.schedule_datetime import ScheduleDatetime
from database.models.user import UserProfile

book_route = Blueprint('book', __name__, template_folder="routes")

@book_route.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == "POST": 
        try:
            schedule_datetime_id= request.form["val"]
            # update target Schedule_datetime with current_user.id 
            target_schedule=ScheduleDatetime.query.filter_by(id=schedule_datetime_id).first()
            target_schedule.user_booking_slot=current_user.id
            db.session.commit()
            return render_template('book_success.html', id=schedule_datetime_id, user=current_user.id)
        except TemplateNotFound: return abort(404)
    return render_template('book_success.html')