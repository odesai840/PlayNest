# defines data models
# run pip install flask-sqlalchemy psycopg2-binary to install sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    forum = db.relationship('Forum', backref=db.backref('threads', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('threads', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    comments = db.relationship('Comment', order_by='Comment.created_at', backref=db.backref('thread_comments', lazy=True, viewonly=True), cascade='all, delete-orphan')

    def __init__(self, title, content, forum_id, user_id):
        self.title = title
        self.content = content
        self.forum_id = forum_id
        self.user_id = user_id

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship('Thread', backref=db.backref('thread_comments', lazy=True, viewonly=True), overlaps="comments")
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent_comment = db.relationship('Comment', remote_side=[id], back_populates='child_comments')
    child_comments = db.relationship('Comment', back_populates='parent_comment', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, content, user_id, thread_id, parent_comment_id=None):
        self.content = content
        self.user_id = user_id
        self.thread_id = thread_id
        self.parent_comment_id = parent_comment_id

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    game_identifier = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_recommendation = db.Column(db.Boolean, nullable=False, default=True)
    rating = db.Column(db.Integer, nullable=True)

    def __init__(self, title, content, user_id, game_identifier, is_recommendation=True, rating=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.game_identifier = game_identifier
        self.is_recommendation = is_recommendation
        self.rating = rating

# added UserProfile model
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    profile_picture = db.Column(db.String(50), default='default.jpg')
    about_me = db.Column(db.String(250))
    
    # add user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # establush relationship with user model
    user_relationship = db.relationship('User', backref='profile', uselist=False)

    def __repr__(self):
        return f'<UserProfile {self.username}>'