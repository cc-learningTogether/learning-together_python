from flask_login import UserMixin


# This file can be deleted if not used I needed for test porpoise UserMixin bring all the function needed from
# flask-login for work (if used in the during the database module creation will make everything easier)
class User(UserMixin):
    def __init__(self, user):
        print(user)
        self.id = user["user_id"]
        self.username = user["username"]
        self.email = user["email"]
