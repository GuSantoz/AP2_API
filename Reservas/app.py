from flask import Flask, jsonify
import requests

app = Flask(__name__)

"""@app.route('/')
def home():
    try:
        # Tenta se comunicar com o microsserviço secundário
        # O nome do host é o nome do serviço definido no docker-compose.yml
        response = requests.get('http://microsservico_secundario:5001/saudacao')
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            mensagem = f"Requisição bem-sucedida! Recebido do Microsserviço Secundário: '{data['mensagem']}' + '{data['nome']}'"
        else:
            mensagem = f"Erro ao se comunicar com o Microsserviço Secundário. Status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        mensagem = f"Erro de conexão com o Microsserviço Secundário: {e}"
    
    return jsonify({"status": "ok", "mensagem_principal": "Olá do Microsserviço Principal!", "resultado_da_comunicacao": mensagem})"""

if __name__ == '__main__':
    app.run(host='0.0.0.0')