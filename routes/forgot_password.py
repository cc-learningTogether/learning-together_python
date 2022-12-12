from flask import Blueprint, render_template, abort, url_for
from jinja2 import TemplateNotFound

from utils.forms import ForgotPswForm
from utils.constants import YEAR, SITE_NAME
from utils.models.auth_manager import AuthManager

forgot_password_route = Blueprint('forgot_password', __name__, template_folder="routes")


@forgot_password_route.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    try:
        form_send_email = ForgotPswForm()
        if form_send_email.validate_on_submit():
            email = form_send_email.email_forgot_password.data
            error = AuthManager(email).forgot_psw()
            if error:
                return render_template("forgot_password.html", message=error, name=SITE_NAME, form=form_send_email,
                                       year=YEAR)
            return render_template("forgot_password.html", message=f"An email has been sent at {email}", name=SITE_NAME,
                                   form=form_send_email, year=YEAR)
        return render_template("forgot_password.html", message="", name=SITE_NAME, form=form_send_email, year=YEAR)
    except TemplateNotFound:
        return abort(404)
