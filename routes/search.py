from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

from datetime import datetime
from utils.forms import SearchForm, DateTimeForm_start, DateTimeForm_finish

from database.db import db
from database.models.schedule_datetime import ScheduleDatetime
from database.models.user import UserProfile

from utils.helper import search_input_handler

search_route = Blueprint('search', __name__, template_folder="routes")


# class SearchManager():
#     def validate_preference(self):
#         try:
#             user = UserProfile(email=self.user_data['email'], user_name=self.user_data['username'],
#                                user_profile_id=user_id,
#                                gender=register_input_handler(self.user_data['gender']),
#                                main_language=register_input_handler(self.user_data['language']),
#                                is_supporter=register_input_handler(self.user_data['is_supporter']))

#             password = UserPassword(user_id=user_id, password=self.user_data['password'])
#             db.session.add(user)
#             db.session.add(password)
#             db.session.commit()
#         except IntegrityError:
#             db.session.rollback()
#             errors = {}
#             if UserProfile.query.filter_by(email=self.user_data['email']).first():
#                 errors['email'] = 'Email already used login please'
#             if UserProfile.query.filter_by(user_name=self.user_data['username']).first():
#                 errors['username'] = 'Username already taken!'
#             if UserProfile.query.filter_by(user_name=self.user_data['password']).first():
#                 return self.register_user(self)
#             return {
#                 'user': '',
#                 'errors': errors
#             }
#         return {
#             'user': user,
#             'errors': '',
#         }


@search_route.route('/search', methods=['GET', 'POST'])
def search():    
    #instantiate form from class 
    dtf_start = DateTimeForm_start() 
    dtf_finish = DateTimeForm_finish()
    form = SearchForm()

    if request.method == 'POST':
        try:
            if current_user.is_authenticated:
                #check each input at datetimepicker
                if dtf_start.validate_on_submit() and dtf_finish.validate_on_submit():
                    dt_start_val= request.form['dt_start']
                    dt_finish_val = request.form['dt_finish']
                    form_language_val = request.form['language']
                    form_gender_val = request.form['gender']
                    #check two inputs at datetimepicker 
                    start_at = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
                    finish_at= datetime.strptime(dt_finish_val, "%Y/%m/%d %H:%M")
                    if ( finish_at- start_at ).total_seconds() < 0 :
                        return render_template('search.html', year=YEAR, 
                        form_start=dtf_start, form_finish=dtf_finish, form_search=form, message="'Finish' should be later than 'Start'")
                    try:
                        #query pair-programming partner
                        # ret = ScheduleDatetime.query
                        # .filter(ScheduleDatetime.start_at >= start_at ).all()
                        ret = ScheduleDatetime.query.join(UserProfile, ScheduleDatetime.user_opening_slot==UserProfile.id).add_columns(ScheduleDatetime.start_at, UserProfile.id, UserProfile.main_language, UserProfile.gender).filter(ScheduleDatetime.start_at >= start_at).filter(UserProfile.main_language==search_input_handler(form_language_val)).all()
                        ## Todo: initialize input 
                        return render_template('search.html', year=YEAR, name=SITE_NAME, 
                        form_start=dtf_start, form_finish=dtf_finish, 
                        form_search=form, result=ret, message=form_language_val)
                    except TemplateNotFound: return abort(404)
                return render_template('search.html', year=YEAR, 
                form_start=dtf_start, form_finish=dtf_finish, form_search=form, message="Validation error")
        except TemplateNotFound: return abort(404)
    else:
        try:
            if current_user.is_authenticated:
                return render_template('search.html', year=YEAR, name=SITE_NAME, form_start=dtf_start, form_finish=dtf_finish, form_search=form)
            return render_template('search.html', year=YEAR, form_start=dtf_start, form_finish=dtf_finish, form_search=form)
        except TemplateNotFound: return abort(404)
