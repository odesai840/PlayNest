import pytest
from app import app, db

@pytest.fixture(scope='module')
def test_app():
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

@pytest.fixture(scope='module', autouse=True)
def clear_db():
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()