from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

# from flask_wtf import FlaskForm
# from wtforms import StringField, ValidationError
# from wtforms.validators import DataRequired
# from datetime import datetime
from utils.forms import SearchForm, DateTimeForm_start, DateTimeForm_finish

from database.db import db
from database.models.schedule_datetime import ScheduleDatetime

from utils.helper import register_input_handler


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
                #to make a schedule
                if dtf_start.validate_on_submit() and dtf_finish.validate_on_submit():
                    dt_start_val= request.form['dt_start']
                    dt_finish_val = request.form['dt_finish']

                    #validate two inputs
                    first = datetime.strptime(dt_start_val, "%Y/%m/%d %H:%M")
                    second = datetime.strptime(dt_finish_val, "%Y/%m/%d %H:%M")
                    if ( second - first ).total_seconds() < 0 :
                        return render_template('search.html', year=YEAR, 
                        form_start=dtf_start, form_finish=dtf_finish, message="Validation error")
                    try:
                        #insert data into db
                        # opening_slot = ScheduleDatetime(start_at = dt_start_val, finish_at = dt_finish_val, user_opening_slot = current_user.id)
                        # db.session.add(opening_slot)
                        # db.session.commit()
                        ## todo: initialize input 
                        return render_template('search.html', year=YEAR, name=SITE_NAME, 
                        form_start=dtf_start, form_finish=dtf_finish, 
                        date_start=dt_start_val, date_finish=dt_finish_val, message="Result")
                    except TemplateNotFound: return abort(404)
                return render_template('search.html', year=YEAR, 
                form_start=dtf_start, form_finish=dtf_finish, message="Validation error")
        except TemplateNotFound: return abort(404)
    else:
        try:
            if current_user.is_authenticated:
                #query user's slots 
                open_slot = ScheduleDatetime.query.filter_by(user_opening_slot=current_user.id).all()
                return render_template('search.html', year=YEAR, name=SITE_NAME, form_start=dtf_start, form_finish=dtf_finish, form_search=form)
            return render_template('search.html', year=YEAR, form_start=dtf_start, form_finish=dtf_finish, form_search=form)
        except TemplateNotFound: return abort(404)
