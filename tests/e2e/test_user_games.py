from flask.testing import FlaskClient
from flask import session

def test_user_games(test_app: FlaskClient):
  # Create a test account
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
      "confirm-password": "password"
  }, follow_redirects=True)
  assert response.status_code == 200

  with test_app.session_transaction() as session:
      session["username"] = "test"
  assert session["username"] == "test"
  # Test that the page loads
  # May require test data first 
