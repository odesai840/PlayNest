from flask.testing import FlaskClient

def test_all_users(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/users')
  assert response.status_code == 200