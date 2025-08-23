import pytest
from datetime import datetime
from flask import Flask
from util import db
from models.team_model import TeamModel
from models.tournament_model import TournamentModel

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()

def test_create_team(session):
    tournament = TournamentModel(
        title="Copa Teste",
        logo="logo.png",
        modality=1, 
        format=2,  
        owner_id=0
    )
    session.add(tournament)
    session.commit()

    team = TeamModel(name="Time A", tournament_id=tournament.id)
    session.add(team)
    session.commit()

    assert team.id is not None
    assert team.name == "Time A"
    assert team.tournament_id == tournament.id
    assert isinstance(team.created_at, datetime)

def test_team_relationship(session):
    tournament = TournamentModel(
        title="Copa Teste",
        logo="logo.png",
        modality=1, 
        format=2,  
        owner_id=0
    )
    session.add(tournament)
    session.commit()

    team = TeamModel(name="Time B", tournament=tournament)
    session.add(team)
    session.commit()

    assert team.tournament == tournament
    assert team in tournament.teams
