from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from models import db, User
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['username'] = username
            return redirect(url_for('home'))
        else: 
            return "Invalid credentials"

    # If it's a GET request, render the login form
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            return "Passwords do not match."
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already in use. Please choose a different one."
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return "Email already in use. Please use a different one."
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    # clear username from session
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

if __name__ == '__main__':
    app.run(debug=True)

