from database.db import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin


class UserProfile(db.Model, UserMixin):
    __tablename__ = 'users_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(UUID(as_uuid=True), unique=True)
    user_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.Integer, default=-1)
    main_language = db.Column(db.Integer, default=-1)
    is_supporter = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "username": self.user_name,
            "email": self.email,
            "gender": self.gender,
            "main_language": self.main_language,
            "is_supporter": self.is_supporter,
            "is_admin": self.is_admin
        }
