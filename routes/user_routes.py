from flask import Blueprint
from controllers.user_controller import (
    create_new_user,
    login_user,
    view_user,
    view_all_users,
    update_user,
    delete_user
)

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")

# Rotas
user_bp.route("/create", methods=["POST"])(create_new_user)
user_bp.route("/login", methods=["POST"])(login_user)
user_bp.route("/users/<int:user_id>", methods=["GET"])(view_user)
user_bp.route("/users", methods=["GET"])(view_all_users)
user_bp.route("/update/<int:user_id>", methods=["PUT"])(update_user)
user_bp.route("/delete/<int:user_id>", methods=["DELETE"])(delete_user)