# Conteúdo do arquivo: app/config.py

class Config:
    # Configurações básicas do Flask
    SECRET_KEY = 'sua_chave_secreta_aqui'
    DEBUG = True # Use False em produção

    # Configuração do Banco de Dados SQLAlchemy
    # Troque o caminho se estiver usando outro DB (PostgreSQL, MySQL, etc.)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///atividade.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

# Se você estiver usando ambientes diferentes (Development, Production), 
# pode ter classes que herdam de Config. Exemplo:
# class DevelopmentConfig(Config):
#     DEBUG = True
#
# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'postgresql://...'