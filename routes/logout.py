from flask import Blueprint, abort, redirect, url_for
from flask_login import logout_user, login_required
from jinja2 import TemplateNotFound

logout_route = Blueprint('logout', __name__, template_folder="routes")


@logout_route.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for("home.home"))
    except TemplateNotFound:
        return abort(404)
