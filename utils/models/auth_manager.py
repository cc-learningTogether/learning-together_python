import uuid
import os
import jwt

from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from database.db import db
from database.models.user import UserProfile
from database.models.password import UserPassword

from utils.helper import register_input_handler, get_reset_token
from utils.email import send_change_password_email


class AuthManager(UserMixin):
    def __init__(self, form_data):
        self.user_data = form_data
        print("user= ", form_data)

    def register_user(self):
        """Take the form data create a new user in the database and return a user object or and error"""
        try:
            user_id = str(uuid.uuid4())

            user = UserProfile(email=self.user_data['email'], user_name=self.user_data['username'],
                               user_profile_id=user_id,
                               gender=register_input_handler(self.user_data['gender']),
                               main_language=register_input_handler(self.user_data['language']),
                               is_supporter=register_input_handler(self.user_data['is_supporter']))

            password = UserPassword(user_id=user_id, password=self.user_data['password'])
            db.session.add(user)
            db.session.add(password)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            errors = {}
            if UserProfile.query.filter_by(email=self.user_data['email']).first():
                errors['email'] = 'Email already used login please'
            if UserProfile.query.filter_by(user_name=self.user_data['username']).first():
                errors['username'] = 'Username already taken!'
            if UserProfile.query.filter_by(user_name=self.user_data['password']).first():
                return self.register_user(self)
            return {
                'user': '',
                'errors': errors
            }
        return {
            'user': user,
            'errors': '',
        }

    def user_login(self):
        """Check if the user is in the database and verify the password"""
        try:
            # verify the presence of the email in the database table
            user = UserProfile.query.filter_by(email=self.user_data['email']).first()
            # raise the exception if no user where found
            if not user:
                raise ValueError('No user found check you email or register a new account')
            # check the password
            user_password = UserPassword.query.filter_by(user_id=str(user.user_profile_id)).first()
            if not check_password_hash(user_password.password, self.user_data['password']):
                raise ValueError('Incorrect password, try again or change your password')
        except ValueError as e:
            return {
                'user': '',
                'errors': e
            }
        return {
            'user': user,
            'errors': '',
        }

    def forgot_psw(self):
        try:
            user = UserProfile.query.filter_by(email=self.user_data).first()
            if not user:
                raise ValueError('No user found check you email or register a new account')
            # token = get_reset_token(user)
            # username = jwt.decode(token,
            #                       key=os.getenv('SECRET_KEY'), algorithms=["HS256"])
            send_change_password_email(user)

        except ValueError as e:
            return e
