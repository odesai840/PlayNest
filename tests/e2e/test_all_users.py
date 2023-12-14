from flask.testing import FlaskClient
from flask import session

def test_all_users(test_app: FlaskClient):
  # Create a test account
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
      "confirm-password": "password"
  }, follow_redirects=True)

  # log in
  with test_app.session_transaction() as session:
      session["username"] = "test"
  assert session["username"] == "test"

  # Test that the page loads
  response = test_app.get('/users')
  assert response.status_code == 200