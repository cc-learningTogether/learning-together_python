from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

home_route = Blueprint('home', __name__, template_folder="routes")


@home_route.route('/')
def home():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
