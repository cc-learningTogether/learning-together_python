from flask import Blueprint, render_template, abort, url_for, redirect
from jinja2 import TemplateNotFound

from utils.forms import ChangePSWForm
from utils.constants import YEAR, SITE_NAME
from utils.helper import verify_reset_token

change_psw_route = Blueprint('change_password', __name__, template_folder='routes')


@change_psw_route.route("/change-password/<string:token>", methods=["POST", "GET"])
def change_password(token):
    try:
        form_change_password = ChangePSWForm()
        try:
            user = verify_reset_token(token)
            if not user:
                raise ValueError('Token expired or not valid')
            if form_change_password.validate_on_submit():
                # TODO check if the 2 password are the same and change the psw i the database
                # TODO decide if login directly or redirect to the login page
                return render_template('index.html', year=YEAR)

            return render_template('change_password.html', year=YEAR, form=form_change_password, name=SITE_NAME)
        except ValueError as e:
            # TODO visualize the error (token expired or not valid) on top of the form
            return redirect(url_for("forgot_password.forgot_password", _external=True))
    except TemplateNotFound:
        abort(404)
