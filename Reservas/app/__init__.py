from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app, template_file="swagger.yml")
    app.config.from_object(Config)
    #app.config['JSON_SORT_KEYS'] = False

    # Inicializa extensões
    db.init_app(app)

    # Importa rotas
    from .routes.route_reservas import registra_reserva

    registra_reserva(app)

    return app