from database.db import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class ScheduleDatetime(db.Model):
    __tablename__ = 'schedules_datetimes'
    id = db.Column(db.Integer, primary_key=True)
    schedule_datetime_id = db.Column(UUID(as_uuid=True), unique=True)
    start_at = db.Column(db.DateTime(timezone=True), nullable=False)
    finish_at = db.Column(db.DateTime(timezone=True), nullable=False)
    user_opening_slot = db.Column(db.Integer, nullable=False)
    user_booking_slot = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
