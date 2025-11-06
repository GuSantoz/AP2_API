from flask import jsonify, request
from ..controllers.aluno_controller import get_alunos, create_aluno, get_aluno_by_id, update_aluno, delete_aluno

def registra_alunos(app):
    @app.route("/alunos", methods=["GET"])
    def listar_alunos():
        alunos = get_alunos()
        #Usando Compreensão de Lista para criar as listas de maneira mais efetiva
        return jsonify([
                {
                    "id": a.id,
                    "nome": a.nome,
                    "idade" : a.idade, "data_nascimento" : a.data_nascimento, "nota_primeiro_semestre" : a.nota_primeiro_semestre, "nota_segundo_semestre" : a.nota_segundo_semestre, "media_final" : a.media_final
                }
                for a in alunos
            ])

    @app.route("/alunos", methods=["POST"])
    def adicionar_aluno():
        data = request.get_json()

        # Valida se turma_id existe
        if "turma_id" not in data:
            return jsonify({"erro": "Campo 'turma_id' é obrigatório"}), 400

        aluno = create_aluno(data)

        if not aluno:
            return jsonify({"erro" : "Erro ao criar aluno"})
        
        return jsonify({
            "id": aluno.id,
            "nome": aluno.nome,
            "idade": aluno.idade,
            "data_nascimento": aluno.data_nascimento,
            "nota_primeiro_semestre": aluno.nota_primeiro_semestre,
            "nota_segundo_semestre": aluno.nota_segundo_semestre,
            "media_final": aluno.media_final,
            "turma_id": aluno.turma_id
        }), 201

    @app.route("/alunos/<int:aluno_id>", methods=["GET"])
    def obter_aluno_id(aluno_id):
        aluno = get_aluno_by_id(aluno_id)
        if not aluno:
            return jsonify({"erro" : "Aluno não encontrado"}), 404
        return({
        "id" : aluno.id,
        "nome" : aluno.nome,
        "idade" : aluno.idade,
        "data_nascimento" : aluno.data_nascimento,
        "nota_primeiro_semestre" : aluno.nota_primeiro_semestre,
        "nota_segundo_semestre" : aluno.nota_segundo_semestre,
        "media_final" : aluno.media_final,
        "turma_id" : aluno.turma_id}), 201

    @app.route("/alunos/<int:aluno_id>", methods=["PUT"])
    def atualizar_aluno(aluno_id):
        data = request.get_json()
        aluno = update_aluno(aluno_id, data)
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404
        return jsonify({
            "id" : aluno.id,
            "nome" : aluno.nome,
            "idade" : aluno.idade,
            "data_nascimento" : aluno.data_nascimento,
            "nota_primeiro_semestre" : aluno.nota_primeiro_semestre,
            "nota_segundo_semestre" : aluno.nota_segundo_semestre,
            "media_final" : aluno.media_final,
            "turma_id" : aluno.turma_id
        }), 201
    
    @app.route("/alunos/<int:aluno_id>", methods=["DELETE"])
    def remover_aluno(aluno_id):
        aluno = delete_aluno(aluno_id)
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404
        return jsonify({"mensagem": f"Aluno {aluno.id} removido com sucesso"}), 201