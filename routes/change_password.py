from flask import Blueprint, render_template, abort, url_for, redirect
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash

from utils.forms import ChangePSWForm
from utils.constants import YEAR, SITE_NAME
from utils.helper import verify_reset_token, password_check
from utils.models.auth_manager import AuthManager

change_psw_route = Blueprint('change_password', __name__, template_folder='routes')


@change_psw_route.route("/change-password/<string:token>", methods=["POST", "GET"])
def change_password(token):
    try:
        form = ChangePSWForm()
        try:
            user = verify_reset_token(token)
            if not user:
                raise ValueError('Token expired or not valid')
            if form.validate_on_submit():
                if password_check(form.password.data):
                    return render_template('change_password.html', name=SITE_NAME, form=form, year=YEAR,
                                           pass_check=password_check(
                                               form.password.data))
                if form.password.data != form.confirm_password.data:
                    return render_template('change_password.html', name=SITE_NAME, form=form, year=YEAR,
                                           pass_check="Password doesn't match")

                AuthManager({"user_id": user.user_profile_id, "password": generate_password_hash(
                    form.password.data,
                    method='pbkdf2:sha256',
                    salt_length=8
                )}).change_password()
                return redirect(url_for("home.home"))

            return render_template('change_password.html', year=YEAR, form=form, name=SITE_NAME)
        except ValueError as e:
            # TODO visualize the error (token expired or not valid) on top of the form
            return redirect(url_for("forgot_password.forgot_password", _external=True))
    except TemplateNotFound:
        abort(404)
