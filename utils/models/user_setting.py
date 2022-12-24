from flask import abort, redirect, url_for
from flask_login import current_user
from sqlalchemy import cast, String
from sqlalchemy.exc import IntegrityError

from database.db import db
from database.models.user import UserProfile


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
            raise ValueError('Email already used!')

        except ValueError as e:
            return e
