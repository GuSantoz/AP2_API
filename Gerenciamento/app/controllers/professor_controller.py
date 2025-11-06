from ..models import Professor, db

def get_professores():
    return Professor.query.all()

def create_professor(data):
    novo = Professor(
        nome=data["nome"],
        idade=data["idade"],
        materia=data["materia"],
        observacoes=data.get("observacoes")
    )

    db.session.add(novo)
    db.session.commit()
    db.session.refresh(novo)  
    return novo

def update_professor(professor_id, data):
    professor = Professor.query.get(professor_id)
    if not professor:
        return None

    professor.nome = data.get("nome", professor.nome)
    professor.idade = data.get("idade", professor.idade)
    professor.materia = data.get("materia", professor.materia)
    professor.observacoes = data.get("observacoes", professor.observacoes)

    db.session.commit()
    return professor

def get_professor_by_id(professor_id):
    return Professor.query.get(professor_id)

def delete_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        return None
    
    db.session.delete(professor)
    db.session.commit()
    return professor
