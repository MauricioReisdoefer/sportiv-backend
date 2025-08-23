import pytest
from datetime import date
from flask import Flask
from util import db
from models.user_model import UserModel
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
        db.session.remove()
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


def test_create_tournament(session):
    # cria usuário dono do torneio
    user = UserModel(
        name="Teste User",
        email="teste@example.com",
        birth_date=date(2000, 1, 1),
        state="SP",
        city="São Paulo",
        username="testuser",
        password_hash="hashed"
    )
    session.add(user)
    session.commit()

    # cria torneio
    tournament = TournamentModel(
        title="Copa Teste",
        logo="logo.png",
        modality=1, 
        format=2,  
        owner_id=user.id
    )
    session.add(tournament)
    session.commit()

    saved = TournamentModel.query.first()
    assert saved is not None
    assert saved.title == "Copa Teste"
    assert saved.logo == "logo.png"
    assert saved.modality == 1
    assert saved.format == 2
    assert saved.owner_id == user.id
    assert saved.owner.username == "testuser"


def test_tournament_repr(session):
    user = UserModel(
        name="Outro User",
        email="outro@example.com",
        birth_date=date(1995, 5, 5),
        state="RJ",
        city="Rio de Janeiro",
        username="outro",
        password_hash="hashed"
    )
    session.add(user)
    session.commit()

    tournament = TournamentModel(
        title="Liga Carioca",
        logo=None,
        modality=0,
        format=1,
        owner_id=user.id
    )
    session.add(tournament)
    session.commit()

    assert "Liga Carioca" in repr(tournament)
    assert f"Owner: {user.id}" in repr(tournament)