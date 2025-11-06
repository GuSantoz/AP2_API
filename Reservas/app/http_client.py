import requests

def get_turma(id):
    url = f"http://localhost:5000/turmas/{id}"
    resposta = requests.get(url, timeout=3)
    return resposta
