from ..models import Turma, db

def get_turmas():
    return Turma.query.all()

def get_turma_by_id(turma_id):
    return Turma.query.get(turma_id)

def create_turma(data):
    novo = Turma(
        descricao=data.get("descricao"),
        professor_id=data["professor_id"],   # obrigatório
        ativo=data["ativo"]                  # obrigatório
    )
    db.session.add(novo)
    db.session.commit()
    return novo

def update_turma(turma_id, data):
    turma = Turma.query.get(turma_id)
    if not turma:
        return None

    turma.descricao = data.get("descricao", turma.descricao)
    turma.professor_id = data.get("professor_id", turma.professor_id)
    turma.ativo = data.get("ativo", turma.ativo)

    db.session.commit()
    return turma

def delete_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return None

    db.session.delete(turma)
    db.session.commit()
    return turma
