from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.database import db, User, Admin
from app.utils.helpers import is_valid_email, hash_password, check_password
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    """Redirect to the login page.
    
    Returns:
        Response: Redirect response to the login page.
    """
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication.
    
    GET: Display the login form.
    POST: Process the login form submission.
    
    Form Parameters:
        username (str): The user's username
        password (str): The user's password
        user_type (str): Type of user ('admin' or 'user')
    
    Returns:
        GET: Rendered login template
        POST: Redirect to appropriate dashboard on success,
             or rendered login template with error message on failure
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        if user_type == 'admin':
            user = Admin.query.filter_by(username=username).first()
        else:
            user = User.query.filter_by(username=username).first()

        if user and check_password(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user_type
            session['username'] = user.username
            if hasattr(user, 'email'):
                session['email'] = user.email
            
            if user_type == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration.
    
    GET: Display the registration form.
    POST: Process the registration form submission.
    
    Form Parameters:
        username (str): Desired username
        email (str): User's email address
        password (str): User's password
        full_name (str): User's full name
        qualification (str): User's qualification
        dob (str): Date of birth in YYYY-MM-DD format
    
    Returns:
        GET: Rendered registration template
        POST: Redirect to login page on successful registration,
             or rendered registration template with error message on failure
    """
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

            hashed_password = hash_password(password)
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
    """Handle user logout.
    
    Clears the user's session and redirects to the login page.
    
    Returns:
        Response: Redirect response to the login page.
    """
    session.clear()
    return redirect(url_for('auth.login')) 