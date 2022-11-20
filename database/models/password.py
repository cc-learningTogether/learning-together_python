from database.db import db
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin


class UserPassword(db.Model, UserMixin):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), unique=True)
    password = db.Column(db.String(100), nullable=False)
