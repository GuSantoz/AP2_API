from .. import db

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.String(100), nullable=False)
    lab = db.Column(db.Boolean, nullable=False)
    data = db.Column(db.String(100), nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
