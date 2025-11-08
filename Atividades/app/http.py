import requests
from requests.exceptions import Timeout, ConnectionError

BASE_URL_GERENCIAMENTO = "http://gerenciamento:5000/" 

def get_turma(id):
    url = f"{BASE_URL_GERENCIAMENTO}turmas/{id}" 
    try:
        resposta = requests.get(url, timeout=3)

        if 400 <= resposta.status_code < 500:
            return None

        if 200 <= resposta.status_code < 300:
            return resposta.json()

        print(f"Erro inesperado do Gerenciamento: Status {resposta.status_code}")
        return None

    except (Timeout, ConnectionError) as e:
        print(f"Erro de comunicação ao buscar Turma {id}: {e}")
        return None

def get_professor(id):
    url = f"{BASE_URL_GERENCIAMENTO}/professores/{id}"
    try:
        resposta = requests.get(url, timeout=3)

        if 200 <= resposta.status_code < 300:
            return resposta.json()

        if 400 <= resposta.status_code < 500:
            return None

        return None

    except (Timeout, ConnectionError) as e:
        print(f"Erro de comunicação ao buscar Professor {id}: {e}")
        return None

def get_aluno(id):
    try:
        url = f"{BASE_URL_GERENCIAMENTO}/alunos/{id}"
        resposta = requests.get(url, timeout=3)

        if 200 <= resposta.status_code < 300:
            return resposta.json()

        if 400 <= resposta.status_code < 500:
            return None

        return None

    except (Timeout, ConnectionError) as e:
        # Lida com erros de rede ou timeout (serviço fora do ar)
        print(f"Erro de comunicação ao buscar Aluno {id}: {e}")
        return None