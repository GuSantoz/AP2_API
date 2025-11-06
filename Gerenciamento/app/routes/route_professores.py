from flask import app,jsonify, request
from ..controllers.professor_controller import get_professores, create_professor, update_professor, get_professor_by_id, delete_professor

def registra_professores(app):
    @app.route("/professores", methods=["GET"])
    def listar_professores():
        professores = get_professores()
        return jsonify([
            {
                "id": p.id,
                "nome": p.nome,
                "idade": p.idade,
                "materia": p.materia,
                "observacoes": p.observacoes
            }
            for p in professores
        ]), 201
    
    @app.route("/professores", methods=["POST"])
    def adicionar_professor():
        data = request.get_json()
        if data is None:
            return jsonify({"erro": "Corpo da requisição vazio ou inválido. Certifique-se de que o Content-Type é application/json."}), 400
        professor = create_professor(data)
        return jsonify({
            "id": professor.id,
            "nome": professor.nome,
            "idade": professor.idade,
            "materia": professor.materia,
            "observacoes": professor.observacoes
        }), 201
    
    @app.route("/professores/<int:professor_id>", methods=["PUT"])
    def atualizar_professor(professor_id):
        data = request.get_json()
        professor = update_professor(professor_id, data)
        if not professor:
            return jsonify({"erro": "Professor nao encontrado"}), 404
        return jsonify({
            "id": professor.id,
            "nome" : professor.nome,
            "idade" : professor.idade,
            "materia" : professor.materia,
            "observacoes": professor.observacoes
        }), 201
    
    @app.route("/professores/<int:professor_id>", methods=["GET"])
    def obter_professor_id(professor_id):
        professor = get_professor_by_id(professor_id)
        if not professor:
            return jsonify({"erro": "Professor nao encontrado"}), 404
        return({
            "id": professor.id,
            "nome" : professor.nome,
            "idade": professor.idade,
            "materia": professor.materia,
            "observacoes": professor.observacoes
        }), 201
    
    @app.route("/professores/<int:professor_id>", methods=["DELETE"])
    def remover_professor(professor_id):
        professor = delete_professor(professor_id)
        if not professor:
            return jsonify({"erro": "Professor nao encontrado"}), 404
        return jsonify({"mensagem": f"Professor {professor.id} removido com sucesso"}), 201
