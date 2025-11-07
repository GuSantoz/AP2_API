from flask import Flask, jsonify

app = Flask(__name__)

"""@app.route('/saudacao')
def saudacao():
    obj = {
        "mensagem": "Olá, sou o Microsserviço Secundário!",
        "nome": "Faculdade Impacta"
    }
    return jsonify(obj)"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)