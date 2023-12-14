from flask.testing import FlaskClient

def test_forum(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/forum')
  assert response.request.path == "/forum"
  assert response.status_code == 200