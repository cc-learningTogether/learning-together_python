from flask import Blueprint, abort, render_template, redirect, url_for
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash

from utils.constants import YEAR, SITE_NAME
from utils.forms import ChangeUsernameForm, UserSettingForm, ChangeEmailForm, ChangeLanguageForm, ChangeGenderForm, \
    ChangeSupporterStatusForm, ChangePSWForm
from utils.helper import favorite_language, set_gender, set_is_supporter, password_check
from utils.models.user_setting import UserSettings

settings_route = Blueprint('settings', __name__, template_folder='routes')


@settings_route.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserSettingForm()
    try:
        if current_user:
            # convert current_user value to string
            language = favorite_language(current_user.main_language)
            gender = set_gender(current_user.gender)
            supporter = set_is_supporter(current_user.is_supporter)
            # initialize the form
            username_form = ChangeUsernameForm()
            email_form = ChangeEmailForm()
            language_form = ChangeLanguageForm()
            gender_form = ChangeGenderForm()
            supporter_form = ChangeSupporterStatusForm()
            password_form = ChangePSWForm()
            # * Set new username
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
                                           language_form=language_form,
                                           email_form=email_form,
                                           gender_form=gender_form,
                                           supporter_form=supporter_form,
                                           email_error="",
                                           name=SITE_NAME,
                                           year=YEAR)
                return redirect(url_for("settings.settings"))
            # * Set new email
            if email_form.validate_on_submit():
                form_data = email_form.email.data
                email_error = UserSettings(form_data).change_email()
                if type(email_error) == str:
                    return render_template("settings.html", user=current_user, language=language[1],
                                           supporter=supporter,
                                           gender=gender[1],
                                           error="",
                                           form=form,
                                           username_error="",
                                           username_form=username_form,
                                           email_form=email_form,
                                           language_form=language_form,
                                           gender_form=gender_form,
                                           email_error=email_error,
                                           supporter_form=supporter_form,
                                           name=SITE_NAME,
                                           year=YEAR)
                return redirect(url_for("settings.settings"))
            # * Set new language
            if language_form.validate_on_submit():
                form_data = language_form.language.data
                UserSettings(form_data).set_language()
                return redirect(url_for("settings.settings"))
            if gender_form.validate_on_submit():
                form_data = gender_form.gender.data
                UserSettings(form_data).set_gender()
                return redirect(url_for("settings.settings"))
            if supporter_form.validate_on_submit():
                form_data = supporter_form.is_supporter.data
                UserSettings(form_data).set_supporter()
                return redirect(url_for("settings.settings"))
            if password_form.validate_on_submit():
                password = password_form.password.data
                confirm_password = password_form.confirm_password.data
                check = password_check(password)
                if not check:
                    if password == confirm_password:
                        hashed_password = generate_password_hash(
                            password,
                            method='pbkdf2:sha256',
                            salt_length=8
                        )
                        UserSettings(hashed_password).update_password()
                        return redirect(url_for("settings.settings"))
                    return render_template("settings.html", user=current_user, language=language[1],
                                           supporter=supporter,
                                           gender=gender[1],
                                           error="",
                                           form=form,
                                           password_form=password_form,
                                           username_error="",
                                           username_form=username_form,
                                           email_form=email_form,
                                           language_form=language_form,
                                           gender_form=gender_form,
                                           email_error="",
                                           pass_error="Password doesn't match",
                                           supporter_form=supporter_form,
                                           name=SITE_NAME,
                                           year=YEAR)
                return render_template("settings.html", user=current_user, language=language[1],
                                       supporter=supporter,
                                       gender=gender[1],
                                       error="",
                                       form=form,
                                       password_form=password_form,
                                       username_error="",
                                       username_form=username_form,
                                       email_form=email_form,
                                       language_form=language_form,
                                       gender_form=gender_form,
                                       email_error="",
                                       pass_error=check,
                                       supporter_form=supporter_form,
                                       name=SITE_NAME,
                                       year=YEAR)
            return render_template("settings.html", user=current_user, language=language[1], supporter=supporter,
                                   gender=gender[1],
                                   error="",
                                   form=form,
                                   password_form=password_form,
                                   language_form=language_form,
                                   email_form=email_form,
                                   username_form=username_form,
                                   gender_form=gender_form,
                                   supporter_form=supporter_form,
                                   name=SITE_NAME,
                                   year=YEAR)
        return abort(403)
    except TemplateNotFound:
        return abort(404)
