import pytest
from app.app import create_app
from app.database.base import Base
from app.database.connection import engine

@pytest.fixture()
def app():
    # Cria uma instância do app em modo de teste
    app = create_app(testing=True)

    # Cria o banco em memória
    Base.metadata.create_all(engine)

    yield app

    # Limpa o banco após os testes
    Base.metadata.drop_all(engine)

@pytest.fixture()
def client(app):
    return app.test_client()