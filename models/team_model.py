from util import db
from datetime import datetime

class TeamModel(db.Model):
    __tablename__ = "teams"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), nullable=False)
    tournament = db.relationship("TournamentModel", backref="teams")
    
    def __repr__(self):
        return f"<Team {self.name} (Tournament: {self.tournament_id})>"