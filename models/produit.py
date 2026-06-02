from datetime import datetime

from extensions import db


class Produit(db.Model):
    """Model Laravel-style : attributs et relations uniquement."""

    __tablename__ = "produits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    prix = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
