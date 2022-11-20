from database.db import db
from sqlalchemy.sql import func


# from sqlalchemy.dialects.postgresql import UUID
# import uuid


class UserProfile(db.Model):
    __tablename__ = 'users_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.String(100), unique=True, nullable=False)
    user_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.Integer, default=-1)
    main_language = db.Column(db.Integer, default=-1)
    is_supporter = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
