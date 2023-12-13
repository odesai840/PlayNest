from flask.testing import FlaskClient
from app import app
from models import User

def tests_signup_page(app):
  # Test that the page loads
  response = app.get('/signup')
  assert response.status_code == 200
  
  # Create a test account
  response = app.post('/signup', data ={
      'username': 'test',
      'email': 'test@gmail.com',
      'password': 'password',
      'confirm_password': 'password'
  }, follow_redirects=True)