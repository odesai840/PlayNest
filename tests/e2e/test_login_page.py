from flask.testing import FlaskClient
from flask import url_for
from models import User

def tests_login_page(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/login')
  assert response.status_code == 200

  # Create a test account
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
      "confirm-password": "password"
  }, follow_redirects=True)

  # Test that log in does not work with incorrect credentials
  response = test_app.post('/login', data ={
    'username': 'wrong',
    'password': 'wrong'
  }, follow_redirects=True)
  assert b"Invalid credentials" in response.data

  # Test that log in works as expected with expected credentials.
  response = test_app.post('/login', data ={
  'username': 'test',
  'password': 'password'
  }, follow_redirects=True)
  assert response.status_code == 200
