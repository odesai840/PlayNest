import pytest

@pytest.fixture
def user_data():
  return[
  {
      'username': 'test',
      'email': 'test@gmail.com',
      'password': 'password',
      'confirm_password': 'password'
  }
  ]