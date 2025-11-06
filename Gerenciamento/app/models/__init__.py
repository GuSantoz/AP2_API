from .. import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.String(200))

    turmas = db.relationship("Turma", backref="professor", lazy=True)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"))
    data_nascimento = db.Column(db.String, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    # media_final = db.Column(db.Float, nullable=False)
    @property
    def media_final(self):
        # Valida se os valores não são None
        if self.nota_primeiro_semestre is None or self.nota_segundo_semestre is None:
            return 0.0
        
        return (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2.0

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100))
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"))
    ativo = db.Column(db.Boolean, nullable=False)

    alunos = db.relationship("Aluno", backref="turma", lazy=True)