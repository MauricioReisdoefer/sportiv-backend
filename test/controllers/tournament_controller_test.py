import pytest
from datetime import date
from flask import Flask
from util import db
from models.user_model import UserModel
from models.tournament_model import TournamentModel
import controllers.torunament_controller as tc

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


@pytest.fixture
def user(session):
    u = UserModel(
        name="Teste User",
        email="teste@example.com",
        birth_date=date(2000, 1, 1),
        state="SP",
        city="São Paulo",
        username="testuser",
        password_hash="hashed"
    )
    session.add(u)
    session.commit()
    return u


def test_create_tournament(session, user):
    t = tc.create_tournament(
        title="Copa Teste",
        logo="logo.png",
        modality=1,
        format=2,
        owner_id=user.id
    )
    assert t.id is not None
    assert t.title == "Copa Teste"
    assert t.logo == "logo.png"
    assert t.owner_id == user.id
    assert t.owner.username == "testuser"


def test_get_tournament_by_id(session, user):
    t = tc.create_tournament("Liga", None, 0, 1, user.id)
    found = tc.get_tournament_by_id(t.id)
    assert found.id == t.id
    assert found.title == "Liga"


def test_get_all_tournaments(session, user):
    tc.create_tournament("T1", None, 0, 1, user.id)
    tc.create_tournament("T2", None, 1, 0, user.id)
    tournaments = tc.get_all_tournaments()
    assert len(tournaments) == 2
    titles = [t.title for t in tournaments]
    assert "T1" in titles and "T2" in titles


def test_update_tournament(session, user):
    t = tc.create_tournament("Old Title", None, 0, 1, user.id)
    updated = tc.update_tournament(t.id, title="New Title", logo="novo_logo.png")
    assert updated.title == "New Title"
    assert updated.logo == "novo_logo.png"


def test_update_nonexistent_tournament(session):
    updated = tc.update_tournament(999, title="Should Fail")
    assert updated is None


def test_delete_tournament(session, user):
    t = tc.create_tournament("Para Deletar", None, 0, 0, user.id)
    result = tc.delete_tournament(t.id)
    assert result is True
    assert tc.get_tournament_by_id(t.id) is None


def test_delete_nonexistent_tournament(session):
    result = tc.delete_tournament(999)
    assert result is False
