from .. import db

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100))
    peso_porcento = db.Column(db.Integer, nullable=False)
    data_entrega = db.Column(db.String(50), nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)

class Notas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)
    atividade_id = db.Column(db.Integer, nullable=False)