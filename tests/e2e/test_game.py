from flask.testing import FlaskClient
from models import User, Game

def test_game(test_app: FlaskClient):
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

  # Check if game was added to database
  games = Game.query.all()
  for game in games:
    assert game.title == 'testgame'
    assert game.game_url == '/static/uploads/testgame'
