from models.tournament_model import TournamentModel
from util import db

# =========================
# Tournament Controller
# =========================

def create_tournament(title, logo, modality, format, owner_id):
    """Cria um novo torneio"""
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
    """Retorna um torneio pelo ID"""
    return TournamentModel.query.get(tournament_id)


def get_all_tournaments():
    """Retorna todos os torneios"""
    return TournamentModel.query.all()


def update_tournament(tournament_id, **kwargs):
    """
    Atualiza campos de um torneio.
    Passar kwargs com os campos a atualizar, ex: title="Novo Título"
    """
    tournament = get_tournament_by_id(tournament_id)
    if not tournament:
        return None

    for key, value in kwargs.items():
        if hasattr(tournament, key):
            setattr(tournament, key, value)

    db.session.commit()
    return tournament


def delete_tournament(tournament_id):
    """Deleta um torneio pelo ID"""
    tournament = get_tournament_by_id(tournament_id)
    if not tournament:
        return False

    db.session.delete(tournament)
    db.session.commit()
    return True
