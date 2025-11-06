from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app, template_file="swagger.yml")
    app.config.from_object(Config)
    app.config['JSON_SORT_KEYS'] = False
    # app.config["OPENAPI_SWAGGER_UI_PATH"] = "/apidocs"

    # Inicializa extensões
    db.init_app(app)
    #Swagger(app)

    # Importa rotas
    from .routes.route_atividades import registra_atividade

    registra_atividade(app)

    return app
