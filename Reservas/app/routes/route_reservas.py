from flask import jsonify, request, app
from ..controllers.reserva_controller import listar_reservas, criar_reserva, atualizar_reserva, deletar_reserva, buscar_reserva_por_id

def registra_reserva(app):
    @app.route('/reservas', methods=['GET'])
    def listar():
        resultado = listar_reservas()
        return jsonify(resultado), 200
    


    @app.route("/reservas/<int:reserva_id>", methods=["GET"])
    def listar_por_id(reserva_id):
        resultado_json, status_code = buscar_reserva_por_id(reserva_id)
        return jsonify(resultado_json), status_code

    @app.route('/reservas', methods=['POST'])
    def criar():
        data = request.get_json()
        resposta, status = criar_reserva(data)
        return jsonify(resposta), status


    @app.route('/reservas/<int:id>', methods=['PUT'])
    def atualizar(id):
        data = request.get_json()
        resposta, status = atualizar_reserva(id, data)
        return jsonify(resposta), status


    @app.route('/reservas/<int:id>', methods=['DELETE'])
    def deletar(id):
        resposta, status = deletar_reserva(id)
        return jsonify(resposta), status