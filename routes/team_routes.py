from controllers.team_controller import (
    create_team,
    get_team_by_id,
    update_team,
    delete_team,
    list_teams,
)
from flask import Blueprint, jsonify

team_bp = Blueprint("team_bp", __name__, url_prefix="/teams")

@team_bp.route("/add", methods=["POST"])
def create_team_route():
    team = create_team()
    return jsonify(team.to_dict()), 201


@team_bp.route("/get/<int:team_id>", methods=["GET"])
def get_team_route(team_id):
    team = get_team_by_id(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(team.to_dict())


@team_bp.route("/update/<int:team_id>", methods=["PUT", "PATCH"])
def update_team_route(team_id):
    team = update_team(team_id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(team.to_dict())


@team_bp.route("/delete/<int:team_id>", methods=["DELETE"])
def delete_team_route(team_id):
    success = delete_team(team_id)
    if not success:
        return jsonify({"error": "Team not found"}), 404
    return jsonify({"message": "Team deleted"})


@team_bp.route("/list", methods=["GET"])
def list_team_route():
    teams = list_teams()
    return jsonify([team.to_dict() for team in teams])
