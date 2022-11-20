from flask import flash
from database.models.user import UserProfile
from database.models.password import UserPassword
from database.db import db
from sqlalchemy.exc import IntegrityError
import uuid


def register_user(form_data):
    """return a user object or and error"""
    try:
        user_id = uuid.uuid4()
        user = UserProfile(email=form_data["email"], user_name=form_data['username'], user_profile_id=user_id,
                           gender=register_input_handler(form_data["gender"]),
                           main_language=register_input_handler(form_data['language']),
                           is_supporter=register_input_handler(form_data['is_supporter']))
        password = UserPassword(user_id=user_id, password=form_data['password'])
        db.session.add(user)
        db.session.add(password)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        errors = {}
        if UserProfile.query.filter_by(email=form_data["email"]).first():
            errors['email'] = "Email already used login please"
        if UserProfile.query.filter_by(user_name=form_data["username"]).first():
            errors['username'] = "Username already taken!"
        if UserProfile.query.filter_by(user_name=form_data["password"]).first():
            return register_user(form_data)
        return {
            'user': "",
            'errors': errors
        }

    return {
        'user': user,
        'errors': "",
    }


def register_input_handler(data):
    if data == '-':
        return
    if data == 'English/英語' or data == 'Male/男':
        return 0
    if data == 'Japanese/日本語' or data == 'Female/女':
        return 1
    if data == 'No/いいえ':
        return False
    if data == "Yes/はい":
        return True
