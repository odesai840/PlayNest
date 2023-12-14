from flask.testing import FlaskClient

def test_forum_threads(test_app: FlaskClient):
  # Create a test account
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
      "confirm-password": "password"
  }, follow_redirects=True)
  assert response.status_code == 200

  test_app.post('/login', data ={
    'username': 'test',
    'password': 'password'
  }, follow_redirects=True)
  assert response.status_code == 200
  # Test that the page loads
  # This will require creating test forum data and loading it here in the future
