from flask.testing import FlaskClient

def test_all_users(test_app: FlaskClient):
  # Create a test account
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
      "confirm-password": "password"
  }, follow_redirects=True)

  # Log in
  response = test_app.post('/login', data ={
    'username': 'test',
    'password': 'password'
  }, follow_redirects=True)

  # Test that the page loads
  response = test_app.get('/users')
  assert response.status_code == 200