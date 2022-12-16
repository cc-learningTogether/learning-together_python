import os
from typing import Tuple

import jwt

from datetime import datetime, timedelta, timezone

from database.models.user import UserProfile

1


def password_check(string):
    if len(string) < 6:
        return 'The password must contain at least 6 characters'
    if len(string) > 10:
        return 'The password must contain max 10 characters'
    return False


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


def favorite_language(val: int) -> Tuple[int, str]:
    """take the value saved in the database and converted it in the correspondent value"""
    if val == -1:
        return 0, "-"
    elif val == 0:
        return 1, 'English/英語'
    elif val == 1:
        return 2, 'Japanese/日本語'


def set_gender(val: int) -> Tuple[int, str]:
    """take the value saved in the database and converted it in the correspondent value"""
    if val == -1:
        return 0, "-"
    elif val == 0:
        return 1, 'Male/男'
    elif val == 1:
        return 2, 'Female/女'


def set_is_supporter(val: bool) -> str:
    if val:
        return 'Yes/はい'
    return 'No/いいえ'


def get_reset_token(user):
    """create the jwt token"""
    return jwt.encode({'reset_password': user.user_name,
                       'exp': datetime(year=datetime.now().year, month=datetime.now().month,
                                       day=datetime.now().day).now(
                           tz=timezone.utc) + timedelta(seconds=5200)},
                      key=os.getenv('SECRET_KEY'))


def verify_reset_token(token):
    """varify the validity of the jwt token sent by email"""
    try:
        username = jwt.decode(token,
                              key=os.getenv('SECRET_KEY'), algorithms="HS256")['reset_password']
    except Exception as e:
        print(e)
        return
    return UserProfile.query.filter_by(user_name=username).first()
