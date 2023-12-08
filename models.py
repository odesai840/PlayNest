# defines data models
# run pip install flask-sqlalchemy psycopg2-binary to install sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta

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
        self.profile = Profile()

class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(255), nullable=True)
    short_description = db.Column(db.String(255), nullable=True)
    long_description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-5))), nullable=False)
    game_url = db.Column(db.String(255), nullable=False)
    author = db.relationship('User', backref='games')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    comments = db.relationship('Comment', order_by='Comment.created_at', backref=db.backref('game_comments', lazy=True, viewonly=True), cascade='all, delete-orphan')

    def __init__(self, title, cover_url, short_description, long_description, game_url, author_id):
        self.title = title
        self.cover_url = cover_url
        self.short_description = short_description
        self.long_description = long_description
        self.game_url = game_url
        self.author_id = author_id

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    forum = db.relationship('Forum', backref=db.backref('threads', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('threads', lazy=True))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-5))), nullable=False)
    comments = db.relationship('Comment', order_by='Comment.created_at', backref=db.backref('thread_comments', lazy=True, viewonly=True), cascade='all, delete-orphan')

    def __init__(self, title, content, forum_id, user_id):
        self.title = title
        self.content = content
        self.forum_id = forum_id
        self.user_id = user_id

    @property
    def profile_picture(self):
        return self.user.profile.profile_picture if self.user and self.user.profile else None

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    game_identifier = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-5))), nullable=False)
    comments = db.relationship('Comment', order_by='Comment.created_at', backref=db.backref('review_comments', lazy=True, viewonly=True), cascade='all, delete-orphan')
    is_recommendation = db.Column(db.Boolean, nullable=False, default=True)
    rating = db.Column(db.Integer, nullable=True)

    def __init__(self, title, content, user_id, game_identifier, is_recommendation=True, rating=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.game_identifier = game_identifier
        self.is_recommendation = is_recommendation
        self.rating = rating

    @property
    def profile_picture(self):
        return self.user.profile.profile_picture if self.user and self.user.profile else None

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship('Thread', backref=db.backref('thread_comments', lazy=True, viewonly=True), overlaps="comments")

    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'))
    review = db.relationship('Review', backref=db.backref('review_comments', lazy=True, viewonly=True), overlaps="comments")

    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    game = db.relationship('Game', backref=db.backref('game_comments', lazy=True, viewonly=True), overlaps="comments")

    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent_comment = db.relationship('Comment', remote_side=[id], back_populates='child_comments')
    child_comments = db.relationship('Comment', back_populates='parent_comment', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-5))), nullable=False)

    def __init__(self, content, user_id, thread_id=None, review_id=None, game_id=None, parent_comment_id=None):
        self.content = content
        self.user_id = user_id
        self.thread_id = thread_id
        self.review_id = review_id
        self.game_id = game_id
        self.parent_comment_id = parent_comment_id

    @property
    def profile_picture(self):
        return self.user.profile.profile_picture if self.user and self.user.profile else None

    def has_liked(self, user_id):
        return any(like.user_id == user_id for like in self.likes)

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('likes', lazy=True, cascade='all, delete-orphan'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    comment = db.relationship('Comment', backref=db.backref('likes', lazy=True, cascade='all, delete-orphan'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    about_me = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    user = db.relationship('User', backref=db.backref('profile', uselist=False), uselist=False)