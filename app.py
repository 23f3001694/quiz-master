from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.database import db, User, Admin
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SECRET_KEY'] = 'your-secret-key' 
db.init_app(app)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        if user_type == 'admin':
            user = Admin.query.filter_by(username=username).first()
        else:
            user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user_type
            if user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        qualification = request.form['qualification']
        dob = request.form['dob']

        if not is_valid_email(username):
            flash('Please enter a valid email address')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Email already registered')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_password,
            full_name=full_name,
            qualification=qualification,
            dob=dob
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Error occurred during registration')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'user':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user)

def create_admin():
    with app.app_context():
        if not Admin.query.filter_by(username='admin@quizmaster.com').first():
            admin = Admin(
                username='admin@quizmaster.com',
                password=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    create_admin()  # Create default admin account
    app.run(debug=True)
