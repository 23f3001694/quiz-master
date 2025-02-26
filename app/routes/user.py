from flask import Blueprint, render_template, session, redirect, url_for
from app.models.database import User
from functools import wraps

user = Blueprint('user', __name__, url_prefix='/user')

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'user':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user.route('/dashboard')
@user_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user) 