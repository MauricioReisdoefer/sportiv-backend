from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models.user_model import UserModel
from util import db

# Criar usuário
def create_new_user():
    data = request.json
    if not data.get("password"):
        return jsonify({"error": "Senha obrigatória"}), 400

    if UserModel.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já cadastrado"}), 400

    if UserModel.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username já cadastrado"}), 400

    user = UserModel(
        name=data["name"],
        email=data["email"],
        birth_date=data["birth_date"],
        state=data.get("state"),
        city=data.get("city"),
        username=data["username"],
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário criado com sucesso"}), 201


# Login
def login_user():
    data = request.json
    user = UserModel.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        # Gera token válido por 1 hora
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Credenciais inválidas"}), 401


# Ver usuário
def view_user(user_id):
    user = UserModel.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "birth_date": str(user.birth_date),
        "state": user.state,
        "city": user.city,
        "username": user.username,
        "created_at": user.created_at.isoformat()
    })


# Ver todos os usuários
def view_all_users():
    users = UserModel.query.all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "username": u.username
        } for u in users
    ])


# Atualizar usuário (precisa estar logado)
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.json
    user = UserModel.query.get_or_404(user_id)

    user.name = data.get("name", user.name)
    user.state = data.get("state", user.state)
    user.city = data.get("city", user.city)

    if data.get("password"):
        user.set_password(data["password"])

    db.session.commit()
    return jsonify({"message": "Usuário atualizado com sucesso"})


# Deletar usuário (precisa estar logado)
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Não autorizado"}), 403

    user = UserModel.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuário deletado com sucesso"})
