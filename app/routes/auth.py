from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.database import db, User, Admin
from app.utils.helpers import is_valid_email
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
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
            session['email'] = user.email
            session['user_id'] = user.id
            session['user_type'] = user_type
            if user_type == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            full_name = request.form['full_name']
            qualification = request.form['qualification']
            dob_str = request.form['dob']

            if not is_valid_email(email):
                flash('Please enter a valid email address')
                return render_template('register.html')

            if User.query.filter_by(email=email).first():
                flash('Email already registered')
                return render_template('register.html')
            
            if User.query.filter_by(username=username).first():
                flash('Username already registered')
                return render_template('register.html')

            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format')
                return render_template('register.html')

            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                full_name=full_name,
                qualification=qualification,
                dob=dob
            )

            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred during registration: {str(e)}')
            return render_template('register.html')

    return render_template('register.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login')) 