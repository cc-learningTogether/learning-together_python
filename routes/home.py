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

@home_route.route('/', methods=['GET', 'POST'])
def home():    
    if request.method == 'POST':
        #delete a schedule 
        slot_id = request.form["val"]
        found_slot = db.session.query(ScheduleDatetime).filter_by(id=slot_id).first()
        db.session.delete(found_slot)
        db.session.commit()

        #query lest of schedules which be opened by current user
        open_slot = ScheduleDatetime.query.filter_by(user_opening_slot=current_user.id).all()

        return render_template('index.html', year=YEAR, name=SITE_NAME, op_slot=open_slot) 

    else:
        try:
            if current_user.is_authenticated:
                #query schedule which be opened by current user
                opening_slot = ScheduleDatetime.query.filter_by(user_opening_slot=current_user.id).all()

                #query schedule which be booked by current user
                booking_slot = ScheduleDatetime.query.filter_by(user_booking_slot=current_user.id).all()

                return render_template('index.html', year=YEAR, name=SITE_NAME, op_slot=opening_slot, bk_slot=booking_slot)
            return render_template('index.html', year=YEAR)
        except TemplateNotFound: return abort(404)
