import requests
from sqlalchemy.exc import IntegrityError
from ..models.atividade import Atividade, Notas, db
from ..http import get_turma, get_professor, get_aluno

#Função para economizar linhas de código
def constroi_atividade(atividade, turma_data=None, professor_data=None):
    return {
        "id": atividade.id,
        "nome_atividade": atividade.nome_atividade,
        "descricao": atividade.descricao,
        "peso_porcento": atividade.peso_porcento,
        "data_entrega": atividade.data_entrega,

        "turma_id": atividade.turma_id,
        "professor_id": atividade.professor_id
    }

#FUNÇÕES ATIVIDADES
def listar_atividades():
    atividades = Atividade.query.all()
    resultado_final = []

    for atividade in atividades:
        turma = get_turma(atividade.turma_id)
        professor = get_professor(atividade.professor_id)

        resultado_final.append(constroi_atividade(atividade, turma, professor))
    return resultado_final

def buscar_atividade_por_id(id):
    atividade = Atividade.query.get(id)

    if not atividade:
        return {"erro": f"Atividade com ID {id} não encontrada."}, 404

    turma = get_turma(atividade.turma_id)
    professor = get_professor(atividade.professor_id)

    resultado = constroi_atividade(atividade, turma, professor)
    return resultado, 200

def criar_atividade(data):
    campos_obrigatorios = ["nome_atividade", "peso_porcento", "data_entrega", "turma_id", "professor_id"]
    for campo in campos_obrigatorios:
        if data.get(campo) is None:
            return {"erro": f"O campo '{campo}' é obrigatório."}, 400

    turma_id = data.get('turma_id')
    professor_id = data.get('professor_id')

    turma = get_turma(turma_id)
    if not turma:
        return {"erro": f"Turma com ID {turma_id} nao encontrada ou microservico indisponvel."}, 404

    professor = get_professor(professor_id)
    if not professor:
        return {"erro": f"Professor com ID {professor_id} não encontrado ou microserviço indisponível."}, 404

    try:
        nova_atividade = Atividade(
            nome_atividade=data["nome_atividade"],
            descricao=data.get("descricao"),
            peso_porcento=data["peso_porcento"],
            data_entrega=data["data_entrega"],
            turma_id=turma_id,
            professor_id=professor_id
        )
        
        db.session.add(nova_atividade)
        db.session.commit()
        
        return {"mensagem": "Atividade criada com sucesso!", "id": nova_atividade.id}, 201

    except IntegrityError:
        db.session.rollback()
        return {"erro": "Erro de integridade no banco de dados."}, 409
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao salvar a atividade: {str(e)}"}, 500

def atualizar_atividade(atividade_id, data):
    atividade = Atividade.query.get(atividade_id)

    if not atividade:
        return {"erro": f"Atividade com ID {atividade_id} não encontrada."}, 404

    #Dicionário para armazenar o ID do campo que precisa de validação HTTP
    ids = {}

    # Executa a validação HTTP para os IDs alterados
    if "id" in ids:
        nova_turma_id = ids["id"]
        if not get_turma(nova_turma_id):
            return {"erro": f"Nova Turma com ID {nova_turma_id} não encontrada."}, 404
        atividade.turma_id = nova_turma_id

    if "id" in ids:
        novo_professor_id = ids["id"]
        if not get_professor(novo_professor_id):
            return {"erro": f"Novo Professor com ID {novo_professor_id} não encontrado."}, 404
        atividade.professor_id = novo_professor_id
    
    # Atualizando os demais campos
    if 'nome_atividade' in data:
        atividade.nome_atividade = data['nome_atividade']
    
    if 'descricao' in data:
        atividade.descricao = data['descricao']

    if 'peso_porcento' in data:
        atividade.peso_porcento = data['peso_porcento']

    if 'data_entrega' in data:
        atividade.data_entrega = data['data_entrega']

    # Tratamento de exceções
    try:
        db.session.commit()
        return {"mensagem": "Atividade atualizada com sucesso.", "id": atividade.id}, 200

    except IntegrityError:
        db.session.rollback()
        return {"erro": "Erro de integridade no banco de dados."}, 409
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao atualizar a atividade: {str(e)}"}, 500

def deletar_atividade(atividade_id):
    atividade = Atividade.query.get(atividade_id)

    if not atividade:
        return {"erro": f"Atividade com ID {atividade_id} não encontrada."}, 404

    try:
        db.session.delete(atividade)
        db.session.commit()

        return {"mensagem": f"Atividade {atividade_id} deletada com sucesso."}, 200

    except Exception as e:
        db.session.rollback()

        return {"erro": f"Erro interno ao deletar a atividade. Certifique-se de que não há notas associadas: {str(e)}"}, 500


#FUNÇÕES NOTAS
def listar_notas(atividade_id):
    if not Atividade.query.get(atividade_id):
        return {"erro": f"Atividade com ID {atividade_id} nao existe."}, 404

    notas = Notas.query.filter_by(atividade_id=atividade_id).all()

    resultado = []
    for n in notas:
        aluno = get_aluno(n.aluno_id) 

        resultado.append({
            "id": n.id,
            "nota": n.nota,
            "aluno": {
                "id": n.aluno_id,
                "nome": aluno.get("nome", "Desconhecido") if aluno else "Desconhecido"
            },
            "atividade_id": n.atividade_id
        })
    return resultado, 200

def criar_nota(atividade_id, data):
    aluno_id = data.get('aluno_id')
    nota_valor = data.get('nota')

    if not all([aluno_id, nota_valor is not None]):
        return {"erro": "Os campos 'aluno_id' e 'nota' são obrigatórios."}, 400

    if not Atividade.query.get(atividade_id):
        return {"erro": f"Atividade {atividade_id} nao encontrada."}, 404

    aluno = get_aluno(aluno_id) 
    if not aluno:
        return {"erro": f"Aluno com ID {aluno_id} nao encontrado ou microserviço indisponivel."}, 404

    try:
        nova_nota = Notas(
            nota=nota_valor,
            aluno_id=aluno_id,
            atividade_id=atividade_id
        )
        db.session.add(nova_nota)
        db.session.commit()
        return {"mensagem": "Nota lancada com sucesso!", "id": nova_nota.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao salvar a nota: {str(e)}"}, 500

def atualizar_nota(nota_id, data):
    nota = Notas.query.get(nota_id)
    if not nota:
        return {"erro": f"Nota com ID {nota_id} não encontrada."}, 404

    if 'nota' in data:
        nota.nota = data['nota']
    
    if 'aluno_id' in data:
        novo_aluno_id = data['aluno_id']
        aluno = get_aluno(novo_aluno_id)
        if not aluno:
            return {"erro": f"Novo Aluno com ID {novo_aluno_id} não encontrado."}, 404
        nota.aluno_id = novo_aluno_id

    try:
        db.session.commit()
        return {"mensagem": f"Nota {nota_id} atualizada com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao atualizar a nota: {str(e)}"}, 500

def deletar_nota(nota_id):
    nota = Notas.query.get(nota_id)
    if not nota:
        return {"erro": f"Nota com ID {nota_id} não encontrada."}, 404

    try:
        db.session.delete(nota)
        db.session.commit()
        return {"mensagem": f"Nota {nota_id} deletada com sucesso."}, 200
    except Exception as e:
        db.session.rollback()
        return {"erro": f"Erro interno ao deletar a nota: {str(e)}"}, 500