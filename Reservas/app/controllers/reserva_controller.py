from ..models.reserva import Reserva, db
import requests
from app.http_client import get_turma

def listar_reservas():
    reservas = Reserva.query.all()
    resultado = []
    for r in reservas:
        turma = get_turma(r.turma_id)
        resultado.append({
            "id": r.id,
            "num_sala": r.num_sala,
            "lab": r.lab,
            "data": r.data,
            "turma_id": r.turma_id,
        })
    return resultado

def buscar_reserva_por_id(reserva_id):
    
    reserva = Reserva.query.get(reserva_id)
    
    if not reserva:
        return {"erro": f"Reserva com ID {reserva_id} não encontrada."}, 404

    turma = get_turma(reserva.turma_id)

    resultado = {
        "id": reserva.id,
        "num_sala": reserva.num_sala,
        "lab": reserva.lab,
        "data": reserva.data,
        "turma_id": reserva.turma_id,
        #"turma_nome": turma.get("nome") if turma else "Turma Desconhecida"
    }
    return resultado, 200

def listar_reserva_id(reserva_id):
    reservas = Reserva.query.all()
    resultado = []
    



def criar_reserva(data):
    turma_id = data.get('turma_id') 
    url = f"http://localhost:5000/turmas/{turma_id}"
    resposta = requests.get(url, timeout=3)

    #turma = get_turma(turma_id)
    if resposta.status_code == 404:
        return {"erro": f"Turma {turma_id} não encontrada"}, 404

    if resposta.status_code == 200 or resposta.status_code == 201:
        nova_reserva = Reserva(
            num_sala=data["num_sala"],
            lab=data["lab"],
            data=data["data"],
            turma_id=turma_id
        )
        db.session.add(nova_reserva)
        db.session.commit()

        return {"mensagem": "Reserva criada com sucesso!"}, 201

def atualizar_reserva(id, data):
    reserva = Reserva.query.get(id)
    if not reserva:
        return {"erro": "Reserva não encontrada"}, 404

    reserva.num_sala = data.get("num_sala", reserva.num_sala)
    reserva.lab = data.get("lab", reserva.lab)
    reserva.data = data.get("data", reserva.data)
    reserva.turma_id = data.get("turma_id", reserva.turma_id)

    db.session.commit()
    return {"mensagem": "Reserva atualizada com sucesso"}, 200


def deletar_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return {"erro": "Reserva não encontrada"}, 404

    db.session.delete(reserva)
    db.session.commit()
    return {"mensagem": "Reserva deletada com sucesso"}, 200