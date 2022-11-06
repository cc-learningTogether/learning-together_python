from database.db import db
from flask_login import UserMixin


# TODO complete the schema with the missing column and relationship
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    email = db.Column(db.String(6000))
    # TODO create the table user_password and instantiate "ONE TO ONE" the relationship
    password = db.Column(db.String(6000))
