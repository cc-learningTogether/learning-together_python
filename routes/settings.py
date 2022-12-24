from flask import Blueprint, abort, render_template, redirect, url_for
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from utils.constants import YEAR, SITE_NAME
from utils.forms import ChangeUsernameForm, UserSettingForm, ChangeEmailForm
from utils.helper import favorite_language, set_gender, set_is_supporter
from utils.models.user_setting import UserSettings

settings_route = Blueprint('settings', __name__, template_folder='routes')


@settings_route.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserSettingForm()
    try:
        if current_user:
            language = favorite_language(current_user.main_language)
            gender = set_gender(current_user.gender)
            supporter = set_is_supporter(current_user.is_supporter)

            username_form = ChangeUsernameForm()
            email_form = ChangeEmailForm()
            if username_form.validate_on_submit():
                form_data = username_form.username.data
                username_message = UserSettings(form_data).change_username()
                if type(username_message) == str:
                    return render_template("settings.html", user=current_user, language=language[1],
                                           supporter=supporter,
                                           gender=gender[1],
                                           error="",
                                           form=form,
                                           username_error=username_message,
                                           username_form=username_form,
                                           email_form=email_form,
                                           email_error="",
                                           name=SITE_NAME,
                                           year=YEAR)
                return redirect(url_for("settings.settings"))
            if email_form.validate_on_submit():
                form_data = email_form.email.data
                email_error = UserSettings(form_data).change_email()
                if email_error:
                    return render_template("settings.html", user=current_user, language=language[1],
                                           supporter=supporter,
                                           gender=gender[1],
                                           error="",
                                           form=form,
                                           username_error="username_message",
                                           username_form=username_form,
                                           email_form=email_form,
                                           email_error=email_error,
                                           name=SITE_NAME,
                                           year=YEAR)

            # TODO split the form
            # form.process()

            return render_template("settings.html", user=current_user, language=language[1], supporter=supporter,
                                   gender=gender[1],
                                   error="",
                                   form=form,
                                   email_form=email_form,
                                   username_form=username_form,
                                   name=SITE_NAME,
                                   year=YEAR)
        return abort(403)
    except TemplateNotFound:
        return abort(404)
