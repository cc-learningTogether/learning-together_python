from flask_login import UserMixin
from database.user import User
from database.db import db
from werkzeug.security import generate_password_hash


# User model it is used for manage all the user action (login register ask or fix meeting

class UserModel(UserMixin):
    def __init__(self, data):
        if data["user_id"]:
            self.id = data["user_id"]
        else:
            self.id = ""
        self.username = data["username"]
        self.email = data["email"]
        # TODO remove the password from here
        self.password = generate_password_hash(data["password"], method='pbkdf2:sha256', salt_length=8)

    def register_user(self):
        """  create a new user need the class to be instantiated and return a user object or and error"""
        if User.query.filter_by(email=self.email).first():
            # TODO user flash message for return the error message (user/email exist, password to short etc )
            return False

        user = User(email=self.email, username=self.username, password=self.password)

        db.session.add(user)
        db.session.commit()
        self.set_id()
        return user

    def set_id(self):
        user = User.query.filter_by(email=self.email).first()
        if user:
            self.id = user.id

    def login(self):
        print("hello")
        return True
