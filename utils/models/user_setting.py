from flask import abort, redirect, url_for
from flask_login import current_user
from sqlalchemy import cast, String
from sqlalchemy.exc import IntegrityError

from database.db import db
from database.models.user import UserProfile
from database.models.password import UserPassword
from utils.helper import input_handler
from utils.email import send_change_password_confirmation


class UserSettings:
    def __init__(self, form_data):
        self.data = form_data

    def change_username(self):
        try:
            user = UserProfile.query.filter(
                cast(UserProfile.user_profile_id, String) == str(current_user.user_profile_id)).first()
            if user and user.user_name != self.data:
                user.user_name = self.data
                db.session.commit()
                return redirect(url_for("settings.settings"))
        except IntegrityError:
            db.session.rollback()
            return "Username already taken!"

    def change_email(self):
        try:
            user = UserProfile.query.filter(
                cast(UserProfile.user_profile_id, String) == str(current_user.user_profile_id)).first()
            if user and user.email != self.data:
                user.email = self.data
                db.session.commit()
                return redirect(url_for("settings.settings"))
        except IntegrityError:
            db.session.rollback()
            return "Email already used!"

    def set_language(self):
        try:
            user = UserProfile.query.filter(
                cast(UserProfile.user_profile_id, String) == str(current_user.user_profile_id)).first()
            if user and user.main_language != self.data:
                user.main_language = register_input_handler(self.data)
                db.session.commit()
                return redirect(url_for("settings.settings"))
            if not user:
                raise ValueError('You are not logged in')
        except ValueError as e:
            return e

    def set_gender(self):
        try:
            user = UserProfile.query.filter(
                cast(UserProfile.user_profile_id, String) == str(current_user.user_profile_id)).first()
            if user and user.gender != self.data:
                user.gender = register_input_handler(self.data)
                db.session.commit()
                return redirect(url_for("settings.settings"))
            if not user:
                raise ValueError('You are not logged in')
        except ValueError as e:
            return e

    def set_supporter(self):
        try:
            user = UserProfile.query.filter(
                cast(UserProfile.user_profile_id, String) == str(current_user.user_profile_id)).first()
            if user and user.is_supporter != self.data:
                user.is_supporter = input_handler(self.data)
                db.session.commit()
                return redirect(url_for("settings.settings"))
            if not user:
                raise ValueError('You are not logged in')
        except ValueError as e:
            return e

    def update_password(self):
        try:
            # check the presence of the user
            user_password = UserPassword.query.filter(
                cast(UserPassword.user_id, String) == str(current_user.user_profile_id)).first()
            if user_password:
                user_password.password = self.data
                db.session.commit()
                user = UserProfile.query.filter(
                    cast(UserProfile.user_profile_id, String) == str(user_password.user_id)).first()
                send_change_password_confirmation(user)
                return True
        except IntegrityError:
            return False
