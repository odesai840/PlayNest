from flask.testing import FlaskClient

def test_game_reviews(test_app: FlaskClient):
  # Test that the page loads
  response = test_app.get('/game_reviews')
  assert response.request.path == "/game_reviews"
  assert response.status_code == 200
