from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user):
        print(user)
        self.id = user["user_id"]
        self.username = user["username"]
        self.email = user["email"]
