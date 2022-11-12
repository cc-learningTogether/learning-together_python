from flask import Blueprint, render_template, abort
from flask_login import login_user, current_user
from utils.user import UserModel
from jinja2 import TemplateNotFound
from utils.form import LoginForm
from utils.constats import year, SITE_NAME

signin_route = Blueprint('signin', __name__, template_folder="routes")


@signin_route.route('/login', methods=["GET", "POST"])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.login_email.data
            print(email)
            # TODO change this part with the database model for the user.py
            #  (user1 e the value you get from the database after the input check)
            # -------- test data --------
            # user = [user for user in users if user["email"] == email][0]
            # user1 = UserModel(user)  # this class can be used for the input check or can be deleted
            # -------------------------
            # login_user(user1)
            # TODO redirect to the page where the user data are
            return render_template('index.html', year=year, current_user=current_user)
        return render_template('sign_in.html', name=SITE_NAME, form=form, year=year, current_user=current_user)
    except TemplateNotFound:
        abort(404)
