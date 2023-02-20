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

book_route = Blueprint('book', __name__, template_folder="routes")

@book_route.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    print("hello")
    dtf_start = DateTimeForm(dt_finish="") # default value for dt_finish
    form = SearchForm()
    if request.method == "POST": 
        try:
            return render_template('book.html')
        except TemplateNotFound: return abort(404)
