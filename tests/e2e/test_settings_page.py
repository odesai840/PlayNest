from flask.testing import FlaskClient
from flask import session
from models import User

def tests_settings_page(test_app: FlaskClient):  
    # Test that the page doesn't load when not logged in
    response = test_app.get('/settings')
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
    
    # Test that the page loads
    response = test_app.get('/settings')
    assert response.status_code == 200

    # test change-email functionality
    response = test_app.post('/change-email', data ={
        "oldemail": "test@gmail.com",
        "newemail": "test1@gmail.com"
    }, follow_redirects=True)
    assert response.status_code == 200

    # test delete-account functionality
    response = test_app.post('/delete-account', data ={
        "delete-account-pw": "password",
    }, follow_redirects=True)
    assert response.status_code == 200

