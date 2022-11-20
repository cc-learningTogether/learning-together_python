from database.db import db
from sqlalchemy.dialects.postgresql import UUID


class UserPassword(db.Model):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), unique=True)
    password = db.Column(db.String(100), nullable=False)
