from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_login import logout_user, current_user
from utils.constats import year

logout_route = Blueprint('logout', __name__, template_folder="routes")


@logout_route.route('/logout', methods=["GET", "POST"])
def logout():
    try:
        logout_user()
        return render_template('index.html', year=year, current_user=current_user)
    except TemplateNotFound:
        abort(404)
