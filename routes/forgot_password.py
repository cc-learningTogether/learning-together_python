from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from utils.forms import ForgotPswForm
from utils.constants import YEAR, SITE_NAME

forgot_password_route = Blueprint('forgot_password', __name__, template_folder="routes")


@forgot_password_route.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    try:
        form_send_email = ForgotPswForm()
        if form_send_email.validate_on_submit():
            email = form_send_email.email
            # TODO verify the presence of the email on the database and send email (Flask email or other)
            return render_template("forgot_password.html", name=SITE_NAME, form=form_send_email, year=YEAR)
        return render_template("forgot_password.html", name=SITE_NAME, form=form_send_email, year=YEAR)
    except TemplateNotFound:
        return abort(404)
