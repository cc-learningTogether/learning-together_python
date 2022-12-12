from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import logout_user, current_user
from jinja2 import TemplateNotFound

from utils.constants import YEAR

logout_route = Blueprint('logout', __name__, template_folder="routes")


@logout_route.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        logout_user()
        return redirect(url_for("home.home"))
    except TemplateNotFound:
        return abort(404)
