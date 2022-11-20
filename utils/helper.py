from flask import flash
from database.models.user import UserProfile
from database.models.password import UserPassword
from database.db import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
import uuid


def register_user(form_data):
    """Take the register user from data create a new user in the database and return a user object or and error"""
    try:
        user_id = str(uuid.uuid4())
        user = UserProfile(email=form_data['email'], user_name=form_data['username'], user_profile_id=user_id,
                           gender=register_input_handler(form_data['gender']),
                           main_language=register_input_handler(form_data['language']),
                           is_supporter=register_input_handler(form_data['is_supporter']))
        password = UserPassword(user_id=user_id, password=form_data['password'])
        db.session.add(user)
        db.session.add(password)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        errors = {}
        if UserProfile.query.filter_by(email=form_data['email']).first():
            errors['email'] = 'Email already used login please'
        if UserProfile.query.filter_by(user_name=form_data['username']).first():
            errors['username'] = 'Username already taken!'
        if UserProfile.query.filter_by(user_name=form_data['password']).first():
            return register_user(form_data)
        return {
            'user': '',
            'errors': errors
        }
    return {
        'user': user,
        'errors': '',
    }


def register_input_handler(data):
    """take a input value from the register form and return a Integer"""
    if data == '-':
        return
    if data == 'English/英語' or data == 'Male/男':
        return 0
    if data == 'Japanese/日本語' or data == 'Female/女':
        return 1
    if data == 'No/いいえ':
        return False
    if data == 'Yes/はい':
        return True


def user_login(form_data):
    print(form_data)
    """Check if the user is in the database and verify the password"""
    try:
        # verify the presence of the email in the database table
        user = UserProfile.query.filter_by(email=form_data['email']).first()
        # raise the exception if no user where found
        if not user:
            raise ValueError('No user found check you email or register a new account')
        # check the password
        user_password = UserPassword.query.filter_by(user_id=str(user.user_profile_id)).first()
        if not check_password_hash(user_password.password, form_data['password']):
            raise ValueError('Incorrect password, try again or change your password')
    except ValueError as e:
        print(type(str(e)))
        return {
            'user': '',
            'errors': e
        }
    return {
        'user': user,
        'errors': '',
    }
