from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
# bcrypt is a hashing library used to securely hash passwords
# instead of storing passwords directly in the database, we store a hash of the password so that if the database is compromised,
# attackers wont have access to the actual user passwords
# make sure virtual environment is activated, then run pip install Flask-Bcrypt to install bcrypt
from flask_bcrypt import Bcrypt
from sqlalchemy import desc
from models import db, User, Forum, Thread, Comment, Review, Game
# pip install requests
import requests

# beautifulsoup4: python package for parsing HTML
# I had an issue where the game descriptions from the API were displaying html elements in the text,
# like <p> and <br> were showing. So I used this package to remove that.
# pip install beautifulsoup4
from bs4 import BeautifulSoup

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

def get_game_details_from_rawg_api(game_id):
    API_KEY = os.getenv('API_KEY')
    base_url = f'https://api.rawg.io/api/games/{game_id}'
    
    params = {
        'key': API_KEY,
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            game_data = response.json()
            
            if 'description' in game_data:
                game_data['description'] = strip_html_tags(game_data['description'])

            return game_data
        else:
            print(f"Error: Unable to fetch game details from RAWG API. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

@app.get('/')
def home():
    # retrieve most recent threads from all forums and recent reviews posted
    recent_threads = Thread.query.order_by(desc(Thread.created_at)).limit(4).all()
    recent_reviews = Review.query.order_by(desc(Review.created_at)).limit(4).all()

    for thread in recent_threads:
        thread.detail_url = url_for('thread_detail', forum_slug=thread.forum.slug, thread_id=thread.id)
    
    for review in recent_reviews:
        review.detail_url = url_for('game_details', game_id=review.game_identifier)
    
    return render_template('home.html', recent_threads=recent_threads, recent_reviews=recent_reviews, get_game_details_from_rawg_api=get_game_details_from_rawg_api)

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

@app.get('/logout')
def logout():
    # clear username from session
    session.pop('username', None)
    return redirect(url_for('home'))

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

@app.route('/settings')
def settings():
    # retrieve user ID of current session user
    user_email = User.query.filter_by(username=session['username']).first().email

    if request.method == 'POST':
        pass
    return render_template('settings.html', user_email=user_email)

@app.route('/change-username', methods=['GET', 'POST'])
def change_username():
    if request.method == 'POST':
        user = User.query.filter_by(username=session['username']).first()
        new_username = request.form['username']
        user.username = new_username
        db.session.commit()

        session['username'] = new_username
    return redirect(url_for('settings'))

@app.route('/change-email', methods=['GET', 'POST'])
def change_email():
    if request.method == 'POST':
        user = User.query.filter_by(username=session['username']).first()
        old_email = request.form['oldemail']
        new_email = request.form['newemail']
        if user.email != old_email:
            return "Current email does not match."
        user.email = new_email
        db.session.commit()
    return redirect(url_for('settings'))

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == "POST":
        old_password = request.form['old-password']
        new_password = request.form['new-password']
        re_new_password = request.form['renew-password']
        user = User.query.filter_by(username=session['username']).first()
        if bcrypt.check_password_hash(user.password_hash, old_password):
            if new_password != re_new_password:
                return "Passwords do not match."
            # hash password before storing it
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password_hash = hashed_password
            db.session.commit()
        else:
            return "Current password incorrect."
    return redirect(url_for('settings'))

@app.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    if request.method == "POST":
        password_verification = request.form['delete-account-pw']
        user = User.query.filter_by(username=session['username']).first()
        if bcrypt.check_password_hash(user.password_hash, password_verification):
            db.session.delete(user)
            db.session.commit()
            # clear username from session
            session.pop('username', None)
    else:
        return "Password incorrect."
    return redirect(url_for('home'))
    
@app.route('/delete-games', methods=['GET', 'POST'])
def delete_games():
    if request.method == "POST":
        password_verification = request.form['delete-games-pw']
        user = User.query.filter_by(username=session['username']).first()
        if bcrypt.check_password_hash(user.password_hash, password_verification):
            user_game = Game.query.filter_by(author_id=user._id).first()
            while user_game != None:
                db.session.delete(user_game)
                db.session.commit()
                user_game = Game.query.filter_by(author_id=user._id).first()
    else:
        return "Password incorrect."
    return redirect(url_for('settings'))

@app.get('/forum')
def forum():
    forums = Forum.query.all()
    return render_template('forum.html', forums=forums)

@app.route('/forum/<forum_slug>', methods=['GET', 'POST'])
def forum_threads(forum_slug):
    # retrieve forum using provided slug from URL 
    forum = Forum.query.filter_by(slug=forum_slug).first()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # retrieve user ID of current session user
        user_id = User.query.filter_by(username=session['username']).first().id
        
        # creating a new thread to add to database
        new_thread = Thread(title=title, content=content, forum_id=forum.id, user_id=user_id)
        db.session.add(new_thread)
        db.session.commit()
    
    # attach URLs to each thread for thread details viewing
    threads = Thread.query.filter_by(forum_id=forum.id).all()
    for thread in threads:
        thread.detail_url = url_for('thread_detail', forum_slug=forum.slug, thread_id=thread.id)

    return render_template('forum_threads.html', forum=forum, threads=threads)

def get_comment_depth(comment, depth=0):
    if comment.parent_comment:
        return get_comment_depth(comment.parent_comment, depth + 1)
    return depth

@app.route('/forum/<forum_slug>/<int:thread_id>', methods=['GET', 'POST'])
def thread_detail(forum_slug, thread_id):
    forum = Forum.query.filter_by(slug=forum_slug).first()
    thread = Thread.query.get(thread_id)
    
    if request.method == 'POST':
        # extract comment info from submitted form data
        content = request.form['content']
        user_id = User.query.filter_by(username=session['username']).first().id
        
        parent_comment_id = request.form.get('parent_comment_id')
        
        # creating a new comment to add to database
        if parent_comment_id:
            new_comment = Comment(content=content, user_id=user_id, thread_id=thread.id, parent_comment_id=parent_comment_id)
        else:
            new_comment = Comment(content=content, user_id=user_id, thread_id=thread.id)
        db.session.add(new_comment)
        db.session.commit()
        
    # Get comments with depth information
    comments = thread.comments
    for comment in comments:
        comment.depth = get_comment_depth(comment)
        comment.indent_class = f"indent-{comment.depth}"
        
    return render_template('thread_detail.html', forum=forum, thread=thread)

@app.route('/forum/<forum_slug>/<int:thread_id>/post_reply', methods=['POST'])
def post_reply(forum_slug, thread_id):
    if request.method == 'POST':
        content = request.form.get('content')
        parent_comment_id = request.form.get('parent_comment_id')
        
        user_id = User.query.filter_by(username=session['username']).first().id
        
        new_comment = Comment(content=content, user_id=user_id, thread_id=thread_id, parent_comment_id=parent_comment_id)
        db.session.add(new_comment)
        db.session.commit()
    
        return redirect(url_for('thread_detail', forum_slug=forum_slug, thread_id=thread_id))


@app.route('/forum/<forum_slug>/<int:thread_id>/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(forum_slug, thread_id, comment_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    comment = Comment.query.get(comment_id)
    
    # check if logged in user is the owner of the comment
    if comment.user.username == session['username']:
        # delete child comments first
        for child_comment in comment.child_comments:
            db.session.delete(child_comment)
            
        db.session.delete(comment)
        db.session.commit()
    
    return redirect(url_for('thread_detail', forum_slug=forum_slug, thread_id=thread_id))

@app.route('/forum/<forum_slug>/<int:thread_id>/edit_comment/<int:comment_id>', methods=['POST'])
def edit_comment(forum_slug, thread_id, comment_id):
    if 'username' not in session: 
        return redirect(url_for('login'))
    comment = Comment.query.get(comment_id)
    
    # check if logged in user is owner of the comment
    if comment.user.username == session['username']:
        if request.method == 'POST':
            new_content = request.form.get('edit_content')
            
            # update the comment content in the database
            comment.content = new_content
            db.session.commit()

    return redirect(url_for('thread_detail', forum_slug=forum_slug, thread_id=thread_id))

@app.route('/forum/<forum_slug>/<int:thread_id>/edit_thread', methods=['POST'])
def edit_thread(forum_slug, thread_id):
    if 'username' not in session: 
        return redirect(url_for('login'))
    
    thread = Thread.query.get(thread_id)
    
    # check if logged in user is the owner of the reply
    if thread.user.username == session['username']:
        if request.method == 'POST':
            new_content = request.form.get('edit_content')
            
            # update the reply content in the database
            thread.content = new_content
            db.session.commit()

    return redirect(url_for('thread_detail', forum_slug=forum_slug, thread_id=thread_id))

@app.route('/forum/<forum_slug>/<int:thread_id>/delete_thread', methods=['POST'])
def delete_thread(forum_slug, thread_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    thread = Thread.query.get(thread_id)
    
    # check if logged in user is the owner of the thread
    if thread.user.username == session['username']:
        # delete all associated comments first
        for comment in thread.comments:
            db.session.delete(comment)
    
        db.session.delete(thread)
        db.session.commit()

    return redirect(url_for('forum_threads', forum_slug=forum_slug))

def get_games_from_rawg_api():
    API_KEY = os.getenv('API_KEY')
    base_url = 'https://api.rawg.io/api/games'
    
    # defining parameters for API request
    params = {
        'key': API_KEY,
        'ordering': '-metacritic',
        'page_size': 12,  # number of games per 'page'
        'language': 'english',
    }
    
    try:
        # make a GET request to RAWG API
        response = requests.get(base_url, params=params)
        
        # checking if request was successful
        if response.status_code == 200:
            # parse the JSON data from the response
            games_data = response.json()
            
            # extract results containing game information
            games = games_data.get('results', [])
            
            return games
        else:
            # print error message is request wasn't successful
            print(f"Error: Unable to fetch games from RAWG API. Status code: {response.status_code}")
            return None
        
    except requests.RequestException as e:
        # print error message if there is an exception during the request
        print(f"Error: {e}")
        return None

@app.get('/game_reviews')
def game_reviews():
    games = get_games_from_rawg_api()
    api_key = os.getenv("API_KEY")
    
    if games is not None and games:
        return render_template('game_reviews.html', games=games, api_key=api_key)
    else:
        # return template without passing the game variable
        return render_template('game_reviews.html')

@app.route('/game_details/<int:game_id>', methods=['GET', 'POST'])
def game_details(game_id):
    game = get_game_details_from_rawg_api(game_id)
    reviews = Review.query.filter_by(game_identifier=str(game_id)).all()
    if game:
        return render_template('review_details.html', game=game, reviews=reviews)
    else:
        return render_template('review_details.html')

def strip_html_tags(html):
    # using BeautifulSoup to parse the HTML and then get text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

@app.route('/post_review', methods=['POST'])
def post_review():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = User.query.filter_by(username=session['username']).first().id
        game_id = request.form.get('game_id')
        is_recommendation = bool(int(request.form.get('recommendation', 1)))
        
        # associate the review with the corresponding game using game_id
        new_review = Review(
            title=title, 
            content=content, 
            user_id=user_id, 
            game_identifier=game_id,
            is_recommendation=is_recommendation
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        # redirect to game details page
        return redirect(url_for('game_details', game_id=game_id))
    
    return redirect(url_for('home'))

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    review = Review.query.get(review_id)
    
    # check if logged in user is owner of the review
    if review.user.username == session['username']:
        db.session.delete(review)
        db.session.commit()
    
    game_id = review.game_identifier
    return redirect(url_for('game_details', game_id=game_id))

@app.route('/edit_review/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    if 'username' not in session: 
        return redirect(url_for('login'))
    
    review = Review.query.get(review_id)
    
    # check if logged in user is the owner of the review
    if review.user.username == session['username']:
        if request.method == 'POST':
            new_content = request.form.get('edit_content')
            
            # update the review content in the database
            review.content = new_content
            db.session.commit()

    game_id = review.game_identifier
    return redirect(url_for('game_details', game_id=game_id))

if __name__ == '__main__':
    app.run(debug=True)

