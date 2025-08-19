import pytest
from util import db
from models import UserModel
from flask import Flask
from datetime import date 

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session

# --- Testes ---
def test_create_user(session):
    user = UserModel(
        name="Maurício",
        email="mauricio@email.com",
        birth_date=date(2009, 1, 1), 
        state="SP",
        city="São Paulo",
        username="mauricio"
    )
    user.set_password("minhasenha123")
    session.add(user)
    session.commit()

    assert user.id is not None
    assert user.password_hash != "minhasenha123"

def test_check_password(session):
    user = UserModel(
        name="Test",
        email="test@email.com",
        birth_date=date(2000, 1, 1), 
        username="testuser",
        state="RJ",
        city="Rio"
    )
    user.set_password("senha123")
    session.add(user)
    session.commit()

    assert user.check_password("senha123") is True
    assert user.check_password("outrasenha") is False

def test_unique_email(session):
    user1 = UserModel(
        name="User1",
        email="unique@email.com",
        birth_date=date(2000, 1, 1),
        username="user1"
    )
    user1.set_password("123")
    session.add(user1)
    session.commit()

    user2 = UserModel(
        name="User2",
        email="unique@email.com",
        birth_date=date(2000, 1, 1),  
        username="user2"
    )
    user2.set_password("123")
    session.add(user2)
    
    with pytest.raises(Exception):  
        session.commit()
