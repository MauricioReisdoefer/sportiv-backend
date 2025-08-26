from models.team_model import TeamModel
from util import db
from flask import request


def create_team() -> TeamModel:
    data = request.get_json()
    name = data.get("name")
    tournament_id = data.get("tournament_id")
    logo = data.get("logo")

    team = TeamModel(name=name, tournament_id=tournament_id, logo=logo)
    db.session.add(team)
    db.session.commit()
    return team


def get_team_by_id(team_id: int) -> TeamModel | None:
    return TeamModel.query.get(team_id)


def update_team(team_id: int) -> TeamModel | None:
    team = TeamModel.query.get(team_id)
    if not team:
        return None

    data = request.get_json()
    name = data.get("name")
    logo = data.get("logo")
    tournament_id = data.get("tournament_id")

    if name is not None:
        team.name = name
    if logo is not None:
        team.logo = logo
    if tournament_id is not None:
        team.tournament_id = tournament_id

    db.session.commit()
    return team


def delete_team(team_id: int) -> bool:
    team = TeamModel.query.get(team_id)
    if not team:
        return False

    db.session.delete(team)
    db.session.commit()
    return True


def list_teams() -> list[TeamModel]:
    return TeamModel.query.all()
