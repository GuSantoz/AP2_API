from flask import jsonify, request
from ..controllers.turma_controller import  get_turmas, get_turma_by_id, create_turma, update_turma, delete_turma

def registra_turmas(app):
    @app.route("/turmas", methods=["GET"])
    def listar_turmas():
        turmas = get_turmas()
        return jsonify([
            {
                "id": t.id,
                "descricao": t.descricao,
                "professor_id": t.professor_id,
                "ativo": t.ativo
            }
            for t in turmas
        ]), 201

    @app.route("/turmas", methods=["POST"])
    def adicionar_turma():
        data = request.get_json()

        if "professor_id" not in data:
            return jsonify({"erro": "Campo 'professor_id' é obrigatório"}), 400
        if "ativo" not in data:
            return jsonify({"erro": "Campo 'ativo' é obrigatório"}), 400

        turma = create_turma(data)
        return jsonify({
            "id": turma.id,
            "descricao": turma.descricao,
            "professor_id": turma.professor_id,
            "ativo": turma.ativo
        }), 201


    @app.route("/turmas/<int:turma_id>", methods=["GET"])
    def obter_turma_id(turma_id):
        turma = get_turma_by_id(turma_id)
        if not turma:
            return jsonify({"erro": "Turma não encontrada"}), 404
        return jsonify({
            "id": turma.id,
            "descricao": turma.descricao,
            "professor_id": turma.professor_id,
            "ativo": turma.ativo
        }), 201

    @app.route("/turmas/<int:turma_id>", methods=["PUT"])
    def atualizar_turma(turma_id):
        data = request.get_json()
        turma = update_turma(turma_id, data)
        if not turma:
            return jsonify({"erro": "Turma não encontrada"}), 404
        return jsonify({
            "id": turma.id,
            "descricao": turma.descricao,
            "professor_id": turma.professor_id,
            "ativo": turma.ativo
        }), 201

    @app.route("/turmas/<int:turma_id>", methods=["DELETE"])
    def remover_turma(turma_id):
        turma = delete_turma(turma_id)
        if not turma:
            return jsonify({"erro": "Turma não encontrada"}), 404
        return jsonify({"mensagem": f"Turma {turma.id} removida com sucesso"}), 201