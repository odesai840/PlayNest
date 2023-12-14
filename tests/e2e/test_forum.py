from flask.testing import FlaskClient

def test_forum(test_app: FlaskClient):

  # Test that the page loads
  response = test_app.get('/forum')
  assert response.request.path == "/forum"
  assert response.status_code == 200 

  # test that a forum loads 
  response = test_app.get('/forum/random-corner')

  # test that a thread cannot be created when not logged in 
  response = test_app.post('/forum/random-corner', data ={
        "title": "test",
        "content": "test"
    }, follow_redirects=True)
  assert response.status_code != 200

  # Create a test account
  response = test_app.post('/signup', data ={
      "username": "test",
      "email": "test@gmail.com",
      "password": "password",
      "confirm-password": "password"
  }, follow_redirects=True)

  # log in
  with test_app.session_transaction() as session:
      session["username"] = "test"
  assert session["username"] == "test"


  