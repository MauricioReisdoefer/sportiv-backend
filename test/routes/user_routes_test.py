import pytest
from flask import Flask
from util import db
from models.user_model import UserModel
from routes.user_routes import user_bp
from flask_jwt_extended import JWTManager, create_access_token
import datetime

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test-secret"
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_user(app):
    def _create_user(email="user@example.com", username="user123", password="123456"):
        with app.app_context():
            user = UserModel(
                name="Test User",
                email=email,
                username=username,
                birth_date=datetime.date(2000, 1, 1)
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # garante que o id seja atribuído antes do commit
            db.session.commit()
            return user.id
    return _create_user

@pytest.fixture
def access_token(app, create_user):
    def _token(email="token@example.com", username="tokenuser"):
        user_id = create_user(email=email, username=username)
        with app.app_context():
            token = create_access_token(identity=user_id)
        return user_id, token
    return _token

def test_create_user(client):
    data = {
        "name": "Mauricio",
        "email": "test@example.com",
        "username": "mauricio123",
        "password": "123456",
        "birth_date": "2000-01-01",
        "state": "SP",
        "city": "São Paulo"
    }
    response = client.post("/user/create", json=data)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data["message"] == "Usuário criado com sucesso"

def test_login_user(client, create_user):
    user_id = create_user(email="login@example.com", username="loginuser", password="123456")
    response = client.post(
        "/user/login", 
        json={"email": "login@example.com", "password": "123456"}
    )
    json_data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in json_data

def test_view_user(client, create_user):
    user_id = create_user(email="view@example.com", username="viewuser")
    response = client.get(f"/user/users/{user_id}")
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["username"] == "viewuser"

def test_view_all_users(client, create_user):
    user1_id = create_user(email="u1@example.com", username="user1")
    user2_id = create_user(email="u2@example.com", username="user2")
    response = client.get("/user/users")
    json_data = response.get_json()
    assert response.status_code == 200
    usernames = [u["username"] for u in json_data]
    assert "user1" in usernames
    assert "user2" in usernames