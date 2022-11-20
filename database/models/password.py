from database.db import db


class UserPassword(db.Model):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
