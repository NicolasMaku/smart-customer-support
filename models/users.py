from datetime import datetime

from extensions import db


class User(db.Model):
    """Model Laravel-style : attributs et relations uniquement."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'agent', 'admin', name='user_roles'), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
