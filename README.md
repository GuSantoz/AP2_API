Criarei o arquivo **`README.md`** completo, cobrindo todos os pontos solicitados, para o seu projeto de Microserviços de Gerenciamento, Atividades e Reservas.

Este README deve ser colocado na raiz do seu repositório AP2.

-----

# 🚀 AP2: Ecossistema de Microserviços Educacionais

Este projeto implementa uma arquitetura de microserviços para gerenciar o ambiente acadêmico, dividida em três serviços independentes: **Gerenciamento** (dados mestres), **Atividades/Notas** (currículo) e **Reservas** (recursos físicos).

## 💡 1. Arquitetura e Estrutura do Projeto

### Arquitetura Utilizada: Microserviços

A arquitetura de Microserviços foi adotada para garantir **escalabilidade**, **independência de deploy** e **isolamento de falhas**. Cada serviço é um processo Python/Flask independente, com seu próprio banco de dados SQLite (`.db`), acessível via API RESTful.

### Ecossistema de Microserviços (Entidades Centrais)

O sistema é composto pelos seguintes serviços, conforme o diagrama ER:

| Serviço | Porta Padrão | Responsabilidade | Entidades Gerenciadas |
| :--- | :--- | :--- | :--- |
| **Gerenciamento** | `5000` | Dados mestres e cadastro base. | `Professor`, `Turma`, `Aluno`. |
| **Atividades / Notas** | `5002` | Gerenciamento curricular e avaliações. | `Atividade`, `Notas`. |
| **Reservas** | `5001` | Agendamento de recursos (salas, labs). | `Reservas`. |

## 🔗 2. Integração e Comunicação entre Serviços

A comunicação entre os serviços é realizada estritamente via **HTTP** (API RESTful), seguindo o princípio de *Dependency Inversion* e garantindo o desacoplamento.

### Padrão Utilizado: Consulta de Chave Estrangeira (FK Lookup)

Os serviços que dependem de dados mestres (FKs) do **Gerenciamento** implementam um módulo `http_client.py` para consultar esses dados no momento necessário:

| Serviço Chamador | Rota Chamada (Gerenciamento) | Propósito |
| :--- | :--- | :--- |
| **Atividades/Notas** | `GET /turmas/{id}` | Valida a existência da `turma_id` em novas atividades. |
| **Atividades/Notas** | `GET /professores/{id}` | Valida a existência do `professor_id` em novas atividades. |
| **Atividades/Notas** | `GET /alunos/{id}` | Valida a existência do `aluno_id` ao lançar notas. |
| **Reservas** | `GET /turmas/{id}` | Valida a existência da `turma_id` em novas reservas. |

**Exemplo de Fluxo (Criação de Atividade):**

1.  O cliente envia um `POST /atividades` (com `turma_id=1` e `professor_id=5`).
2.  O Microserviço de Atividades **não** acessa o DB do Gerenciamento.
3.  O Atividades envia uma requisição `GET http://127.0.0.1:5000/turmas/1`.
4.  O Gerenciamento retorna `200 OK` (dados da Turma).
5.  O Atividades envia uma requisição `GET http://127.0.0.1:5000/professores/5`.
6.  O Gerenciamento retorna `200 OK` (dados do Professor).
7.  Se todas as validações forem bem-sucedidas, a Atividade é salva no DB local do serviço Atividades.

## 📄 3. Descrição da API (Endpoints Principais)

Todos os serviços expõem sua documentação completa via **Swagger UI** (Flasgger).

### Microserviço: Gerenciamento (Porta `5000`)

| Recurso | Método | Rota | Descrição |
| :--- | :--- | :--- | :--- |
| Turma | `GET` | `/turmas` | Lista turmas. |
| Turma | `GET` | `/turmas/{id}` | Busca turma por ID. |
| Professor | `GET` | `/professores` | Lista professores. |
| Professor | `GET` | `/professores/{id}` | Busca professor por ID. |
| Aluno | `GET` | `/alunos` | Lista alunos. |
| Aluno | `POST` | `/alunos` | Cria um novo aluno. |
| **Documentação** | `GET` | `/apidocs` | Swagger UI. |

### Microserviço: Atividades/Notas (Porta `5002`)

| Recurso | Método | Rota | Descrição |
| :--- | :--- | :--- | :--- |
| Atividade | `GET` | `/atividades` | Lista atividades. |
| Atividade | `POST` | `/atividades` | Cria atividade (Valida FKs via HTTP). |
| Atividade | `GET/PUT/DEL` | `/atividades/{id}` | CRUD por ID. |
| Notas | `GET/POST` | `/atividades/{id}/notas` | Lançar/Listar notas para uma atividade. |
| Notas | `PUT/DEL` | `/notas/{id}` | Atualiza/Deleta um lançamento de nota. |
| **Documentação** | `GET` | `/apidocs` | Swagger UI. |

### Microserviço: Reservas (Porta `5001`)

| Recurso | Método | Rota | Descrição |
| :--- | :--- | :--- | :--- |
| Reservas | `GET` | `/reservas` | Lista reservas. |
| Reservas | `POST` | `/reservas` | Cria reserva (Valida FKs via HTTP). |
| Reservas | `GET/PUT/DEL` | `/reservas/{id}` | CRUD por ID. |
| **Documentação** | `GET` | `/apidocs` | Swagger UI. |

## ⚙️ 4. Instruções de Execução (com Docker)

Para garantir a execução de todo o ecossistema de forma isolada e simplificada, utilize o Docker Compose.

### Pré-requisitos

1.  **Docker** e **Docker Compose** instalados.

### Passos de Execução

1.  **Crie o Dockerfile e o `docker-compose.yml`**
    (Você precisará criar um `Dockerfile` e um `docker-compose.yml` na raiz do projeto).

    > **Exemplo Simples de `docker-compose.yml`:**

    > ```yaml
    > version: '3.8'
    > services:
    >   gerenciamento:
    >     build: ./Gerenciamento
    >     ports: ["5000:5000"]
    >     volumes: ["./Gerenciamento:/app"]
    > ```

    > reservas:
    > build: ./Reservas
    > ports: ["5001:5001"]
    > volumes: ["./Reservas:/app"]
    > depends\_on: [gerenciamento] \# Garante que Gerenciamento suba primeiro

    > atividades:
    > build: ./Atividades
    > ports: ["5002:5002"]
    > volumes: ["./Atividades:/app"]
    > depends\_on: [gerenciamento] \# Garante que Gerenciamento suba primeiro

    > ```
    > ```

2.  **Construa e Inicie os Contêineres**
    A partir da raiz do projeto, execute o comando (leva alguns minutos na primeira vez):

    ```bash
    docker compose up --build -d
    ```

3.  **Verifique o Status**

    ```bash
    docker compose ps
    ```

    Todos os serviços (`gerenciamento`, `reservas`, `atividades`) devem estar com o status `Up`.

4.  **Acesse a Documentação**
    Você pode agora acessar as APIs e a documentação:

      * **Gerenciamento:** `http://localhost:5000/apidocs`
      * **Reservas:** `http://localhost:5001/apidocs`
      * **Atividades:** `http://localhost:5002/apidocs`

5.  **Desligar os Serviços**

    ```bash
    docker compose down
    ```