from database.db import db


# This class is for a test. You can remove this class.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
