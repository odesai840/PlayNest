from flask.testing import FlaskClient
from app import app
from models import User

def tests_login_page(app):
  # Test that the page loads
  response = app.get('/login')
  assert response.status_code == 200

  # Create a test account
  response = app.post('/signup', data ={
      'username': 'test',
      'email': 'test@gmail.com',
      'password': 'password',
      'confirm_password': 'password'
  }, follow_redirects=True)

  # Test that log in does not work with incorrect credentials
  response = app.post('/login', data ={
    'username': 'wrong',
    'password': 'wrong'
  }, follow_redirects=True)
  assert b"Invalid credentials" in response.data

  # Test that log in works as expected with expected credentials.
  response = app.post('/login', data ={
    'username': 'test',
    'password': 'password'
  }, follow_redirects=True)
  assert b"Invalid credentials" not in response.data
  assert response.status_code == 200