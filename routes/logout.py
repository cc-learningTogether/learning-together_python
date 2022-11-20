from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from utils.constants import YEAR

logout_route = Blueprint('logout', __name__, template_folder="routes")


@logout_route.route('/logout', methods=['POST'])
def logout():
    try:
        print("Bye")
        return render_template('index.html', year=YEAR)
    except TemplateNotFound:
        return abort(404)
