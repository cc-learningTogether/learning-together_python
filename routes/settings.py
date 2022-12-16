from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from utils.constants import YEAR, SITE_NAME
from utils.forms import UserSettingForm
from utils.helper import favorite_language, set_gender, set_is_supporter

settings_route = Blueprint('settings', __name__, template_folder='routes')


@settings_route.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    try:
        if current_user:
            language = favorite_language(current_user.main_language)
            gender = set_gender(current_user.gender)
            supporter = set_is_supporter(current_user.is_supporter)
            form = UserSettingForm()
            # TODO split the form
            form.process()

            return render_template("settings.html", user=current_user, language=language[1], supporter=supporter,
                                   gender=gender[1],
                                   form=form, name=SITE_NAME,
                                   year=YEAR)
        return abort(403)
    except TemplateNotFound:
        return abort(404)
