from flask import Blueprint, abort, render_template
from flask_login import current_user
from jinja2 import TemplateNotFound

from utils.constants import YEAR, SITE_NAME

settings_route = Blueprint('settings', __name__, template_folder='routes')


@settings_route.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        return render_template("setting.html", user=current_user, name=SITE_NAME, year=YEAR)
    except TemplateNotFound:
        return abort(404)
