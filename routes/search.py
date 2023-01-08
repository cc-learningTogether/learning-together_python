from flask import Blueprint, render_template, abort, request
from flask_login import current_user, login_required 
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from datetime import datetime
from utils.forms import SearchForm, DateTimeForm

from database.db import db
from database.models.schedule_datetime import ScheduleDatetime
from database.models.user import UserProfile

from utils.helper import search_input_handler

search_route = Blueprint('search', __name__, template_folder="routes")

@search_route.route('/search', methods=['GET', 'POST'])
@login_required
def search():    
    #instantiate form from class 
    dtf_start = DateTimeForm() 
    dtf_finish = 0; # default value 
    form = SearchForm()

    if request.method == 'POST':
        try:
            #check each input at datetimepicker
            if dtf_start.validate_on_submit():
                #datetime input from form
                dt_start_val= request.form['dt_start']
                start_at = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
                #language input from form
                form_language_val = request.form['language']
                #gender input from form 
                form_gender_val = request.form['gender']
                #is_supporter input from form 
                form_is_supporter_val = request.form['is_supporter']
                try:
                    #query pair-programming partner (! datetime and language are must)
                    #if gender and is_supporter are not chosen
                    if search_input_handler(form_gender_val) == -1 and search_input_handler(form_is_supporter_val) == -1:
                        schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, UserProfile.id, UserProfile.main_language).filter(ScheduleDatetime.start_at <= start_at).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.id!=current_user.id).all()
                    #if gender is not chosen 
                    elif search_input_handler(form_gender_val) == -1:
                        schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, UserProfile.id, UserProfile.main_language, UserProfile.is_supporter).filter(ScheduleDatetime.start_at <= start_at).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.is_supporter==search_input_handler(form_is_supporter_val)).filter(UserProfile.id!=current_user.id).all()
                    # if is_supporter is not chosen 
                    elif search_input_handler(form_is_supporter_val) == -1:
                        schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, UserProfile.id, UserProfile.main_language, UserProfile.gender).filter(ScheduleDatetime.start_at <= start_at).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.gender==search_input_handler(form_gender_val)).filter(UserProfile.id!=current_user.id).all()
                    # if all conditions are chosen 
                    else:
                        schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, UserProfile.id, UserProfile.main_language, UserProfile.gender, UserProfile.is_supporter).filter(ScheduleDatetime.start_at <= start_at).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.gender==search_input_handler(form_gender_val)).filter(UserProfile.is_supporter==search_input_handler(form_is_supporter_val)).filter(UserProfile.id!=current_user.id).all()
                    ## Todo: initialize input 
                    return render_template('search.html', year=YEAR, name=SITE_NAME, 
                    form_start=dtf_start, 
                    form_search=form, result=schedule_list, message=form_language_val)
                except TemplateNotFound: return abort(404)
        except TemplateNotFound: return abort(404)
    else:
        try:
            return render_template('search.html', year=YEAR, name=SITE_NAME, form_start=dtf_start, form_search=form)
        except TemplateNotFound: return abort(404)
