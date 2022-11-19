from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from utils.constant import YEAR

home_route = Blueprint('home', __name__, template_folder="routes")


@home_route.route('/')
def home():
    try:
        return render_template('index.html', year=YEAR)
    except TemplateNotFound:
        return abort(404)
