from flask.testing import FlaskClient
from models import User

def tests_signup_page(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/signup')
  assert response.status_code == 200
  
  # Create a test account
  response = test_app.post('/signup', data ={
      'username': 'test',
      'email': 'test@gmail.com',
      'password': 'password',
      'confirm_password': 'password'
  }, follow_redirects=True)