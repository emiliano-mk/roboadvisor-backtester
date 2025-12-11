from datetime import datetime
from app.extensions import db

class Transaction(db.Model):
    __tablename__ = "portfolio_transactions"

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(32), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    tx_type = db.Column(db.String(8), nullable=False)  # BUY / SELL
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(255))
