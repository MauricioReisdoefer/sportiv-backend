from util import db
from datetime import datetime

class TournamentModel(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    modality = db.Column(db.Integer, nullable=False)  # Enum
    format = db.Column(db.Integer, nullable=False)    # Enum

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("UserModel", backref="tournaments")

    def __repr__(self):
        return f"<Tournament {self.title} (Owner: {self.owner_id})>"
