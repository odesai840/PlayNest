from flask.testing import FlaskClient
from flask import session
from models import User, Game

def test_user_games(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/user_games')
  assert response.request.path == "/user_games"
  assert response.status_code == 200

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

  # Test publishing a game
  response = test_app.post('/dashboard', data = {
    'title': 'testgame',
    'game-file': b'testgame.zip'
  }, follow_redirects=True)
  assert response.status_code == 200
  
  # Check if game was added to database and is displayed on page
  games = Game.query.all()
  for game in games:
    assert game.title == 'testgame'
    assert game.game_url == '/static/uploads/testgame'
    response = test_app.get('/user_games')
    assert b'testgame' in response.data
