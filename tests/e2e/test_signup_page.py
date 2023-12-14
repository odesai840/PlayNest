from flask.testing import FlaskClient
from models import User

def tests_signup_page(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/signup')
  assert response.status_code == 200

  # test that an account be created if it is missing information 
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
  }, follow_redirects=True)
  assert response.status_code != 200

  # Create a test account
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
      "confirm-password": "password"
  }, follow_redirects=True)

  assert response.status_code == 200

  # test that a user was added to the db
  Users = User.query.all()
  for user in Users:
    assert user.username == "test"
    assert user.email == "test@gmail.com"