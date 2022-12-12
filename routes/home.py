from flask import Blueprint, render_template, abort
from flask_login import current_user
from jinja2 import TemplateNotFound
from utils.constants import YEAR, SITE_NAME

home_route = Blueprint('home', __name__, template_folder="routes")


@home_route.route('/')
def home():
    try:
        if current_user.is_authenticated:
            return render_template('index.html', year=YEAR, name=SITE_NAME)
        return render_template('index.html', year=YEAR)
    except TemplateNotFound:
        return abort(404)
