import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.team_model import TeamModel
from models.tournament_model import TournamentModel
from controllers.team_controller import (
    create_team, get_team_by_id, update_team, delete_team, list_teams
)
from util import db

@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        
@pytest.fixture(scope="function")
def session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
        
@pytest.fixture
def tournament(session):
    t = TournamentModel(title="Copa Teste", modality="Futebol", format="Eliminatório", owner_id=1)
    session.add(t)
    session.commit()
    return t

# --- Testes ---
def test_create_team(session, tournament):
    team = create_team(name="Time A", tournament_id=tournament.id, logo="logo.png")
    assert team.id is not None
    assert team.name == "Time A"
    assert team.logo == "logo.png"
    assert team.tournament_id == tournament.id

def test_get_team_by_id(session, tournament):
    team = create_team(name="Time B", tournament_id=tournament.id)
    fetched = get_team_by_id(team.id)
    assert fetched is not None
    assert fetched.id == team.id

def test_update_team(session, tournament):
    team = create_team(name="Time C", tournament_id=tournament.id)
    updated = update_team(team.id, name="Time C Updated", logo="new_logo.png")
    assert updated.name == "Time C Updated"
    assert updated.logo == "new_logo.png"

def test_update_team_not_found(session):
    updated = update_team(9999, name="Não Existe")
    assert updated is None

def test_delete_team(session, tournament):
    team = create_team(name="Time D", tournament_id=tournament.id)
    result = delete_team(team.id)
    assert result is True
    assert get_team_by_id(team.id) is None

def test_delete_team_not_found(session):
    result = delete_team(9999)
    assert result is False

def test_list_teams(session, tournament):
    team1 = create_team(name="Time E1", tournament_id=tournament.id)
    team2 = create_team(name="Time E2", tournament_id=tournament.id)
    all_teams = list_teams()
    assert len(all_teams) >= 2
    ids = [t.id for t in all_teams]
    assert team1.id in ids
    assert team2.id in ids
