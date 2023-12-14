from flask.testing import FlaskClient
from flask import session

def test_profile_view(test_app: FlaskClient):
    response = test_app.get('/view_own_profile')
    assert response.status_code != 200
    # Create a test account
    response = test_app.post('/signup', data ={
        "username": "test",
        "email": "test@gmail.com",
        "password": "password",
        "confirm-password": "password"
    }, follow_redirects=True)
    assert response.status_code == 200
    # log in
    with test_app.session_transaction() as session:
        session["username"] = "test"
    assert session["username"] == "test"

    response = test_app.get('/view_own_profile')
    assert response.status_code == 200
