from flask.testing import FlaskClient
from models import User, Game

def test_dashboard(test_app: FlaskClient):
  # Test that the page cannot be accessed without logging in
  response = test_app.get('/dashboard')
  assert response.status_code != 200

  # Create a test account and log in
  response = test_app.post('/signup', data ={
    "username": "test",
    "email": "test@gmail.com",
    "password": "password",
    "confirm-password": "password"
  }, follow_redirects=True)

  with test_app.session_transaction() as session:
    session["username"] = "test"
  assert session["username"] == "test"

  # Test that the page can be accessed after logging in
  response = test_app.get('/dashboard')
  assert response.status_code == 200

  # Test publishing game with no game title
  response = test_app.post('/dashboard', data = {
    'game-file': b'test.zip'
  }, follow_redirects=True)
  assert response.status_code == 400

  # Test publishing a game with no cover
  response = test_app.post('/dashboard', data = {
    'title': 'test',
    'game-file': b'test.zip'
  }, follow_redirects=True)
  assert response.status_code == 200

  # Test publishing a game with all form fields filled
  response = test_app.post('/dashboard', data = {
    'title': 'test',
    'short-description': 'test',
    'long-description': 'test',
    'cover-image': b'test.png',
    'game-file': b'test.zip'
  }, follow_redirects=True)
  assert response.status_code == 200

  # Test unsupported file type handling
  # Unsupported game file type
  response = test_app.post('/dashboard', data = {
    'title': 'test',
    'game-file': b'test.png'
  }, follow_redirects=True)
  # This should return status code 200 if the route
  # returns "Invalid game file format"
  assert response.status_code == 200

  # Unsupported cover file type
  response = test_app.post('/dashboard', data = {
    'title': 'test',
    'cover-image': b'test.zip',
    'game-file': b'test.zip'
  }, follow_redirects=True)
  # This should return status code 200 if the route
  # sets the game cover to the default image
  assert response.status_code == 200