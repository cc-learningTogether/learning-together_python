from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from utils.forms import ChangePSWForm
from utils.constants import YEAR, SITE_NAME

change_psw_route = Blueprint('change_password', __name__, template_folder='routes')


@change_psw_route.route("/change-password/<string:token>", methods=["POST", "GET"])
def change_password(token):
    try:
        # TODO verify the token
        form_change_password = ChangePSWForm()
        if form_change_password.validate_on_submit():
            # TODO check if the 2 password are the same and change the psw i the database
            # TODO decide if login directly or redirect to the login page
            pass
            return render_template('index.html', year=YEAR)
        return render_template("change_password.html", name=SITE_NAME, form=form_change_password, year=YEAR)
    except TemplateNotFound:
        abort(404)
