from flask.testing import FlaskClient
from flask import session

def test_user_games(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/user_games')
  assert response.request.path == "/user_games"
  assert response.status_code == 200
