import uuid
import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy import cast, String
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import db
from database.models.user import UserProfile
from database.models.password import UserPassword

from utils.helper import register_input_handler
from utils.email import send_change_password_email, send_change_password_confirmation


def create_admin():
    users = UserProfile.query.all()
    if len(users) == 0 and os.getenv("ADMIN_EMAIL"):
        user_id = str(uuid.uuid4())
        password = "admin1" if not os.getenv("ADMIN_PASSWORD") else os.getenv("ADMIN_PASSWORD")
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        user = UserProfile(
            email=os.getenv("ADMIN_EMAIL"),
            user_name="admin" if not os.getenv("ADMIN_USERNAME") else os.getenv("ADMIN_USERNAME"),
            user_profile_id=user_id,
            is_supporter=True,
            is_admin=True
        )

        password = UserPassword(user_id=user_id, password=hashed_password)
        db.session.add(user)
        db.session.add(password)
        db.session.commit()

    if not os.getenv("ADMIN_EMAIL"):
        print("The ADMIN_EMAIL must be set in the env file")


class AuthManager(UserMixin):
    def __init__(self, form_data):
        self.user_data = form_data

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
                raise ValueError('No user found check your email or register a new account')
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
        """Send an email to the user or throw an error"""
        try:
            # check the presence of the user in the database
            user = UserProfile.query.filter_by(email=self.user_data).first()
            if not user:
                raise ValueError('No user found check your email or register a new account')
            # send the email with the link for the change password route
            send_change_password_email(user)

        except ValueError as e:
            return e

    def change_password(self):
        try:
            # check the presence of the user
            user_password = UserPassword.query.filter(
                cast(UserPassword.user_id, String) == str(self.user_data['user_id'])).first()
            if user_password:
                user_password.password = self.user_data['password']
                db.session.commit()
                user = UserProfile.query.filter(
                    cast(UserProfile.user_profile_id, String) == str(user_password.user_id)).first()
                send_change_password_confirmation(user)
                login_user(user)
                return True
        except IntegrityError:
            return False
