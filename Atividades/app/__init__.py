from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from .config import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    swagger = Swagger(app, template_file="swagger.yml")
    app.config.from_object(Config)
    app.config['JSON_SORT_KEYS'] = False

    # Inicializa extensões
    db.init_app(app)

    # Importa rotas
    from .routes.route_atividades import registra_atividade

    registra_atividade(app)

    return app
