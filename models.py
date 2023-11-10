# defines data models
# run pip install flask-sqlalchemy psycopg2-binary to install sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash