import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS

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