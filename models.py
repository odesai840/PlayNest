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

class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    game_cover_url = db.Column(db.String(255), nullable=True)
    short_description = db.Column(db.String(255), nullable=True)
    long_description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.String(255), nullable=False)
    game_url = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def __init__(self, title, game_cover_url, short_description, long_description, release_date, game_url, author_id):
        self.title = title
        self.game_cover_url = game_cover_url
        self.short_description = short_description
        self.long_description = long_description
        self.release_date = release_date
        self.game_url = game_url
        self.author_id = author_id