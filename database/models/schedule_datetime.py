from database.db import db
from sqlalchemy.sql import func


class ScheduleDatetime(db.Model):
    __tablename__ = 'schedules_datetimes'
    id = db.Column(db.Integer, primary_key=True)
    start_at = db.Column(db.DateTime(timezone=True), nullable=False)
    finish_at = db.Column(db.DateTime(timezone=True), nullable=False)
    user_opening_slot = db.Column(db.Integer, db.ForeignKey('users_profiles.id'), nullable=False)
    user_booking_slot = db.Column(db.Integer, db.ForeignKey('users_profiles.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
