import os
import jwt

from datetime import datetime, timedelta, timezone

from database.models.user import UserProfile


# def register_user(form_data):
#     """Take the register user from data create a new user in the database and return a user object or and error"""
#     try:
#         user_id = str(uuid.uuid4())
#         user = UserProfile(email=form_data['email'], user_name=form_data['username'], user_profile_id=user_id,
#                            gender=register_input_handler(form_data['gender']),
#                            main_language=register_input_handler(form_data['language']),
#                            is_supporter=register_input_handler(form_data['is_supporter']))
#         password = UserPassword(user_id=user_id, password=form_data['password'])
#         db.session.add(user)
#         db.session.add(password)
#         db.session.commit()
#     except IntegrityError:
#         db.session.rollback()
#         errors = {}
#         if UserProfile.query.filter_by(email=form_data['email']).first():
#             errors['email'] = 'Email already used login please'
#         if UserProfile.query.filter_by(user_name=form_data['username']).first():
#             errors['username'] = 'Username already taken!'
#         if UserProfile.query.filter_by(user_name=form_data['password']).first():
#             return register_user(form_data)
#         return {
#             'user': '',
#             'errors': errors
#         }
#     return {
#         'user': user,
#         'errors': '',
#     }

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

    # def user_login(form_data):
    #     """Check if the user is in the database and verify the password"""
    #     try:
    #         # verify the presence of the email in the database table
    #         user = UserProfile.query.filter_by(email=form_data['email']).first()
    #         # raise the exception if no user where found
    #         if not user:
    #             raise ValueError('No user found check you email or register a new account')
    #         # check the password
    #         user_password = UserPassword.query.filter_by(user_id=str(user.user_profile_id)).first()
    #         if not check_password_hash(user_password.password, form_data['password']):
    #             raise ValueError('Incorrect password, try again or change your password')
    #     except ValueError as e:
    #         return {
    #             'user': '',
    #             'errors': e
    #         }
    #     return {
    #         'user': user,
    #         'errors': '',
    #     }


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
