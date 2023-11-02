from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you can add your authentication logic, such as checking the username and password against a database.
        if username == "admin" and password == "password":
            # storing username in the session
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"

    # If it's a GET request, render the login form
    return render_template('login.html')


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

if __name__ == '__main__':
    app.run(debug=True)

