from flask import Blueprint, abort, redirect, url_for, render_template
from flask_login import login_required
from jinja2 import TemplateNotFound

from utils.decorators import admin_only
from utils.constants import YEAR, SITE_NAME
from database.db import db
from database.models.user import UserProfile

manager_route = Blueprint('manager', __name__, template_folder="routes")


@manager_route.route('/manager', methods=['GET', 'POST'])
@login_required
@admin_only
def manager():
    try:
        users = UserProfile.query.all()
        print(users)
        return render_template("manager_panel.html", name=SITE_NAME, year=YEAR)
        # return redirect(url_for("manager.manager"))
    except TemplateNotFound:
        return abort(404)
