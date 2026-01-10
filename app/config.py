import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# Cria a pasta 'database' se não existir
db_folder = os.path.join(app.root_path, 'database')
os.makedirs(db_folder, exist_ok=True)

# configurando banco de dados sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/database/onebus.db'

# configurando banco de dados
class Base(DeclarativeBase):
    # responsáveis para relacionamento 1:N
    __abstract__ = True
    #__allow_unmapped__ = True

db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs" 
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "OneBus API",
        "description": "API REST para gerenciamento de ônibus e trajetos",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)