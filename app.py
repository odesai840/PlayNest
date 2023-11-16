from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
# bcrypt is a hashing library used to securely hash passwords
# instead of storing passwords directly in the database, we store a hash of the password so that if the database is compromised,
# attackers wont have access to the actual user passwords
# make sure virtual environment is activated, then run pip install Flask-Bcrypt to install bcrypt
from flask_bcrypt import Bcrypt
from models import db, User, Game

# run pip install python-dotenv to install
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
db.init_app(app) # initializing database with the flask app

bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'zip'}

@app.get('/')
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
        
        # validation for password confirmation
        if password != confirm_password:
            return "Passwords do not match."
        
        # checking if username already exists in database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already in use. Please choose a different one."
        
        # checking if email already exists in database
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return "Email already in use. Please use a different one."
        
        # hash password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # creating a new user and inserting it into the database
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        # redirecting to log in page after sign up
        return redirect(url_for('login'))
    
# render the sign up form if GET request
    return render_template('signup.html')

@app.get('/home')
def home():
    return render_template('home.html')

@app.get('/logout')
def logout():
    # clear username from session
    session.pop('username', None)
    return redirect(url_for('index'))

@app.get('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post('/upload')
def upload_game():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # If the line below shows up as an error, just ignore it.
        # It works fine.
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect('/dashboard')

@app.get('/settings')
def settings():
    return render_template('settings.html')

@app.get('/forum')
def forum():
    return render_template('forum.html')