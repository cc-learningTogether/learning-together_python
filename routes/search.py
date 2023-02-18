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
    dtf_start = DateTimeForm(dt_finish="") # default value for dt_finish
    form = SearchForm()
    if dtf_start.validate_on_submit():
        dt_start_val= request.form['dt_start']
        start_at = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
        form_language_val = request.form['language']
        form_gender_val = request.form['gender']
        form_is_supporter_val = request.form['is_supporter']
        # todo もし当日よりも前の日付を選択したら "you can't chose bofore today"と返す
        # date, time and language are must to be given! 
        if form_language_val is "-": 
            return render_template('search.html', year=YEAR, name=SITE_NAME, 
            form_start=dtf_start, 
            form_search=form, result="", message="Please chose 'Language'")
        try:
            #if gender and is_supporter are not chosen
            if search_input_handler(form_gender_val) == -1 and search_input_handler(form_is_supporter_val) == -1:
                schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, ScheduleDatetime.finish_at, UserProfile.id, UserProfile.user_name,UserProfile.main_language, UserProfile.gender, UserProfile.is_supporter,ScheduleDatetime.user_opening_slot, ScheduleDatetime.user_booking_slot).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.id!=current_user.id).all()
            #if gender is not chosen 
            elif search_input_handler(form_gender_val) == -1:
                schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, ScheduleDatetime.finish_at, UserProfile.id, UserProfile.user_name,UserProfile.main_language, UserProfile.gender, UserProfile.is_supporter,ScheduleDatetime.user_opening_slot, ScheduleDatetime.user_booking_slot).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.is_supporter==search_input_handler(form_is_supporter_val)).filter(UserProfile.id!=current_user.id).all()
            # if is_supporter is not chosen 
            elif search_input_handler(form_is_supporter_val) == -1:
                schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, ScheduleDatetime.finish_at, UserProfile.id, UserProfile.user_name,UserProfile.main_language, UserProfile.gender, UserProfile.is_supporter,ScheduleDatetime.user_opening_slot, ScheduleDatetime.user_booking_slot).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.gender==search_input_handler(form_gender_val)).filter(UserProfile.id!=current_user.id).all()
            # if all conditions are chosen 
            else:
                schedule_list = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, ScheduleDatetime.finish_at, UserProfile.id, UserProfile.user_name,UserProfile.main_language, UserProfile.gender, UserProfile.is_supporter,ScheduleDatetime.user_opening_slot, ScheduleDatetime.user_booking_slot).filter(ScheduleDatetime.finish_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).filter(UserProfile.gender==search_input_handler(form_gender_val)).filter(UserProfile.is_supporter==search_input_handler(form_is_supporter_val)).filter(UserProfile.id!=current_user.id).all()

            # 取得したデータを整形し保持し、ページを読み込む
            list = []
            for i in range(len(schedule_list)):
                if schedule_list[i]["user_booking_slot"] == None: # If the slot is open
                    data = {}
                    data["id"] = schedule_list[i]["id"]
                    data["user_name"] = schedule_list[i]["user_name"]
                    # handle main language 
                    if schedule_list[i]["main_language"] == 0:
                        data["main_language"] = "English"
                    elif schedule_list[i]["main_language"] == 1:
                        data["main_language"] = "Japanese"
                    else: 
                        data["main_language"] = "-"
                    # handle gender
                    if schedule_list[i]["gender"] == 0:
                        data["gender"] = "Male"
                    elif schedule_list[i]["gender"] == 1:
                        data["gender"] = "Female"
                    else:
                        data["gender"] = "-"
                    # handle is_supporter
                    if schedule_list[i]["is_supporter"]:
                        data["is_supporter"] = "Supporter"
                    else:
                        data["is_supporter"] = "Not a supporter"
                    data["start_at"] = schedule_list[i]["start_at"].strftime("%Y/%m/%d %H:%M")  
                    data["finish_at"] = schedule_list[i]["finish_at"].strftime("%Y/%m/%d %H:%M")
                    list.append(data) 
                
            return render_template('search.html', year=YEAR, name=SITE_NAME, 
            form_start=dtf_start, 
            form_search=form, result=list, message="succsess")
        except TemplateNotFound: return abort(404)
    else:
        try:
            return render_template('search.html', year=YEAR, name=SITE_NAME, 
            form_start=dtf_start, 
            form_search=form)
        except TemplateNotFound: return abort(404)