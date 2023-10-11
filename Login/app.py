from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Here you can add authentication logic
    if username == "admin" and password == "password":
        return redirect(url_for('index'))
    else:
        return "Invalid credentials"

if __name__ == '__main__':
    app.run(debug=True)
