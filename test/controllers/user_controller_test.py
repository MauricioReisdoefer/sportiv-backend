import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from util import db
from models.user_model import UserModel
from flask_jwt_extended.exceptions import NoAuthorizationError
import datetime

import controllers.user_controller as user_controller


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test-secret"
    app.config["TESTING"] = True

    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def new_user():
    user = UserModel(
        name="Teste",
        email="teste@example.com",
        birth_date=datetime.date(2000, 1, 1),
        username="testeuser",
    )
    user.set_password("1234")
    db.session.add(user)
    db.session.commit()
    return user


def test_create_new_user(app):
    with app.test_request_context(json={
        "name": "Novo",
        "email": "novo@example.com",
        "birth_date": "2000-01-01",
        "username": "novouser",
        "password": "senha"
    }):
        res, code = user_controller.create_new_user()
        assert code == 201
        assert res.get_json()["message"] == "Usuário criado com sucesso"


def test_login_user(app, new_user):
    with app.test_request_context(json={
        "email": "teste@example.com",
        "password": "1234"
    }):
        res, code = user_controller.login_user()
        assert code == 200
        assert "access_token" in res.get_json()


def test_view_user(app, new_user):
    with app.test_request_context():
        res = user_controller.view_user(new_user.id)
        assert res.status_code == 200
        data = res.get_json()
        assert data["username"] == "testeuser"


def test_view_all_users(app, new_user):
    with app.test_request_context():
        res = user_controller.view_all_users()
        assert res.status_code == 200
        data = res.get_json()
        assert isinstance(data, list)
        assert any(u["username"] == "testeuser" for u in data)


def test_update_user_requires_login(app, new_user):
    with app.test_request_context(json={"name": "Hack"}):
        with pytest.raises(NoAuthorizationError):
            user_controller.update_user(new_user.id)


def test_update_user_with_token(app, new_user):
    # 1. login pra gerar token
    with app.test_request_context(json={
        "email": "teste@example.com",
        "password": "1234"
    }):
        login, _ = user_controller.login_user()
        token = login.get_json()["access_token"]

    # 2. update com token
    headers = {"Authorization": f"Bearer {token}"}
    with app.test_request_context(
        json={"name": "Atualizado"},
        headers=headers
    ):
        res = user_controller.update_user(new_user.id)
        assert res.status_code == 200 or res[1] == 200
        assert "Usuário atualizado com sucesso" in str(res.get_json())


def test_delete_user_with_token(app, new_user):
    with app.test_request_context(json={
        "email": "teste@example.com",
        "password": "1234"
    }):
        login, _ = user_controller.login_user()
        token = login.get_json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    with app.test_request_context(headers=headers):
        res = user_controller.delete_user(new_user.id)
        assert res.status_code == 200 or res[1] == 200
        assert res.get_json()["message"] == "Usuário deletado com sucesso"
