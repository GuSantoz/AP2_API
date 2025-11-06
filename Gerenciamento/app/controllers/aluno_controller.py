from ..models import Aluno, db, Turma

def get_alunos():
    return Aluno.query.all()

def get_aluno_by_id(aluno_id):
    return Aluno.query.get(aluno_id)

def create_aluno(data):
    turma= Turma.query.get(data.get("turma_id"))

    if not turma:
        return None

    novo = Aluno(
        nome=data["nome"],
        idade=data["idade"],
        data_nascimento=data["data_nascimento"],
        nota_primeiro_semestre=data["nota_primeiro_semestre"],
        nota_segundo_semestre=data["nota_segundo_semestre"],
        turma_id=data["turma_id"]
    )

    db.session.add(novo)
    db.session.commit()
    db.session.refresh(novo)  # garante que o objeto tenha o ID e todos os campos atualizados

    return novo


def update_aluno(aluno_id, data):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return None

    # Atualiza apenas os campos enviados no body
    aluno.nome = data.get("nome", aluno.nome)
    aluno.idade = data.get("idade", aluno.idade)
    aluno.data_nascimento = data.get("data_nascimento", aluno.data_nascimento)
    aluno.nota_primeiro_semestre = data.get("nota_primeiro_semestre", aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = data.get("nota_segundo_semestre", aluno.nota_segundo_semestre)
    aluno.turma_id = data.get("turma_id", aluno.turma_id)

    db.session.commit()
    return aluno

def delete_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return None
    
    db.session.delete(aluno)
    db.session.commit()
    return aluno