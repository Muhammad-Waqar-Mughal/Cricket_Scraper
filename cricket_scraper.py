from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8467044fdemsh1a4a175854aad63p19cea2jsn5961618649b1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html', name=current_user.username)

@app.route('/scrape', methods=['POST'])
@login_required
def scrape():
    url = "https://free-cricket-live-score1.p.rapidapi.com/schedule/upcoming"
    payload = {
        "page_number": 1,
        "match_formate": "T20"
    }
    headers = {
        "x-rapidapi-key": "8467044fdemsh1a4a175854aad63p19cea2jsn5961618649b1",
        "x-rapidapi-host": "free-cricket-live-score1.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    matches = response.json().get("res", {}).get("matches", [])
    return render_template('results.html', matches=matches)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
