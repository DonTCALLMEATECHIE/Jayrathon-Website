from flask import Flask, render_template, request, redirect, url_for, session, flash
import os, json

app = Flask(__name__)
app.secret_key = "your-secret-key"
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists')
        else:
            users[username] = password
            save_users(users)
            flash('Account created, please sign in')
            return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('courses'))
        else:
            flash('Invalid credentials')
    return render_template('signin.html')

@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect(url_for('landing'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated

@app.route('/courses')
@login_required
def courses():
    return render_template('courses.html', username=session.get('username'))

@app.route('/tools')
@login_required
def tools():
    return render_template('tools.html', username=session.get('username'))

@app.route('/references')
@login_required
def references():
    return render_template('references.html', username=session.get('username'))

@app.route('/resources')
@login_required
def resources():
    return render_template('resources.html', username=session.get('username'))

@app.route('/communities')
@login_required
def communities():
    return render_template('communities.html', username=session.get('username'))

@app.route('/youtube')
@login_required
def youtube():
    return render_template('youtube.html', username=session.get('username'))

@app.route('/practice')
@login_required
def practice():
    return render_template('practice.html', username=session.get('username'))

@app.route('/blogs')
@login_required
def blogs():
    return render_template('blogs.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)