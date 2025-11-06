from flask import request, jsonify

# Importando TODAS as funções do controller
from ..controllers.atividades_controller import (
    listar_atividades, 
    criar_atividade, 
    buscar_atividade_por_id, 
    atualizar_atividade, 
    deletar_atividade,
    listar_notas, 
    criar_nota, 
    atualizar_nota, 
    deletar_nota
)

# Esta função recebe a instância do app e registra todas as rotas
def registra_atividade(app):

    # ROTAS DE ATIVIDADES (CRUD Completo)

    @app.route('/atividades', methods=['GET'])
    def get_atividades_route():
        resultado = listar_atividades()
        return jsonify(resultado), 200

    @app.route('/atividades', methods=['POST'])
    def add_atividade_route():
        data = request.get_json()
        resultado, status_code = criar_atividade(data)
        return jsonify(resultado), status_code

    @app.route('/atividades/<int:id>', methods=['GET'])
    def get_atividade_route(id):
        resultado, status_code = buscar_atividade_por_id(id)
        return jsonify(resultado), status_code

    @app.route('/atividades/<int:id>', methods=['PUT'])
    def edit_atividade_route(id):
        data = request.get_json()
        resultado, status_code = atualizar_atividade(id, data)
        return jsonify(resultado), status_code

    @app.route('/atividades/<int:id>', methods=['DELETE'])
    def remove_atividade_route(id):
        resultado, status_code = deletar_atividade(id)
        return jsonify(resultado), status_code

    #====================================================
    # ROTAS DE NOTAS (CRUD Completo)
    #====================================================

    # GET: /atividades/<atividade_id>/notas (Listar notas de uma atividade)
    # POST: /atividades/<atividade_id>/notas (Criar nova nota para uma atividade)
    @app.route('/atividades/<int:atividade_id>/notas', methods=['GET'])
    def get_notas_route(atividade_id):
        resultado, status_code = listar_notas(atividade_id)
        return jsonify(resultado), status_code

    @app.route('/atividades/<int:atividade_id>/notas', methods=['POST'])
    def add_nota_route(atividade_id):
        data = request.get_json()
        resultado, status_code = criar_nota(atividade_id, data)
        return jsonify(resultado), status_code
        
    # PUT: /notas/<nota_id> (Atualizar nota específica)
    @app.route('/notas/<int:nota_id>', methods=['PUT'])
    def edit_nota_route(nota_id):
        data = request.get_json()
        resultado, status_code = atualizar_nota(nota_id, data)
        return jsonify(resultado), status_code

    # DELETE: /notas/<nota_id> (Deletar nota específica)
    @app.route('/notas/<int:nota_id>', methods=['DELETE'])
    def remove_nota_route(nota_id):
        resultado, status_code = deletar_nota(nota_id)
        return jsonify(resultado), status_code