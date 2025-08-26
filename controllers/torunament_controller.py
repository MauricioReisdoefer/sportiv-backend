from models.tournament_model import TournamentModel
from util import db
from flask import request

def create_tournament():
    data = request.json
    title, logo, modality, format, owner_id = data["title"], data["logo"], data["modality"], data["format"], data["owner_id"]
    tournament = TournamentModel(
        title=title,
        logo=logo,
        modality=modality,
        format=format,
        owner_id=owner_id
    )
    db.session.add(tournament)
    db.session.commit()
    return tournament


def get_tournament_by_id(tournament_id):
    return TournamentModel.query.get(tournament_id)


def get_all_tournaments():
    return TournamentModel.query.all()


def update_tournament(tournament_id, **kwargs):
    tournament = get_tournament_by_id(tournament_id)
    if not tournament:
        return None

    for key, value in kwargs.items():
        if hasattr(tournament, key):
            setattr(tournament, key, value)

    db.session.commit()
    return tournament


def delete_tournament(tournament_id):
    tournament = get_tournament_by_id(tournament_id)
    if not tournament:
        return False

    db.session.delete(tournament)
    db.session.commit()
    return True
