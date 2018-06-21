import os
import pytest
from src.app import create_app
from src.database import get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'r') as f:
    _data_sql = []
    for line in f:
        _data_sql.append(line.strip('\n'))

@pytest.fixture
def app():
    app = create_app('test')
    with app.app_context():
        db = get_db()
        db.run_sql(_data_sql)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


