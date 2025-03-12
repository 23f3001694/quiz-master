import re
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for, flash
from datetime import datetime, date
from sqlalchemy import or_

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'user':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Generate a secure hash of the password"""
    return generate_password_hash(password)

def check_password(hashed_password, password):
    """Check if the password matches the hash"""
    return check_password_hash(hashed_password, password)

def is_quiz_available(quiz):
    """Check if a quiz is currently available based on date and time"""
    current_datetime = datetime.now()
    quiz_date = quiz.date_of_quiz.date()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    
    return (
        quiz_date == current_date and
        quiz.start_time <= current_time <= quiz.end_time
    )

def format_datetime(dt):
    """Format a datetime object to a readable string"""
    if isinstance(dt, datetime):
        return dt.strftime('%B %d, %Y at %I:%M %p')
    elif isinstance(dt, date):
        return dt.strftime('%B %d, %Y')
    return str(dt)

def calculate_percentage(score, max_score):
    """Calculate percentage from score and max score"""
    try:
        if not isinstance(max_score, (int, float)) or max_score <= 0:
            return 0
        return round((score / max_score) * 100, 2)
    except (ZeroDivisionError, TypeError):
        return 0

def validate_form_data(form_data, required_fields):
    """Validate that all required fields are present in form data"""
    missing_fields = []
    for field in required_fields:
        if field not in form_data or not form_data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        flash(f"Missing required fields: {', '.join(missing_fields)}")
        return False
    return True

def get_user_from_session():
    """Get the current user from the session"""
    from app.models.database import User, Admin
    
    if 'user_id' not in session:
        return None
    
    user_type = session.get('user_type')
    user_id = session.get('user_id')
    
    if user_type == 'admin':
        return Admin.query.get(user_id)
    elif user_type == 'user':
        return User.query.get(user_id)
    
    return None

def search_users(query):
    """Search for users by username, email, or full name"""
    from app.models.database import User
    
    return User.query.filter(
        or_(
            User.username.ilike(f'%{query}%'),
            User.email.ilike(f'%{query}%'),
            User.full_name.ilike(f'%{query}%')
        )
    ).all()

def search_subjects(query):
    """Search for subjects by name or description"""
    from app.models.database import Subject
    
    return Subject.query.filter(
        or_(
            Subject.name.ilike(f'%{query}%'),
            Subject.description.ilike(f'%{query}%')
        )
    ).all()

def search_chapters(query):
    """Search for chapters by name or description"""
    from app.models.database import Chapter
    
    return Chapter.query.filter(
        or_(
            Chapter.name.ilike(f'%{query}%'),
            Chapter.description.ilike(f'%{query}%')
        )
    ).all()

def search_quizzes(query):
    """Search for quizzes by related chapter name or duration"""
    from app.models.database import Quiz, Chapter
    
    return Quiz.query.join(Chapter).filter(
        or_(
            Chapter.name.ilike(f'%{query}%'),
            Quiz.time_duration.ilike(f'%{query}%')
        )
    ).all()

def search_questions(query):
    """Search for questions by question statement or options"""
    from app.models.database import Question
    
    return Question.query.filter(
        or_(
            Question.question_statement.ilike(f'%{query}%'),
            Question.option1.ilike(f'%{query}%'),
            Question.option2.ilike(f'%{query}%'),
            Question.option3.ilike(f'%{query}%'),
            Question.option4.ilike(f'%{query}%')
        )
    ).all()

def calculate_score_statistics(user_scores):
    """Calculate score statistics from a list of user scores"""
    total_quizzes = len(user_scores)
    if total_quizzes == 0:
        return {
            'total_quizzes': 0,
            'average_score': 0,
            'best_score': 0,
            'worst_score': 0
        }
    
    try:
        score_percentages = [calculate_percentage(score.total_score, score.max_score) for score in user_scores]
        if not score_percentages:
            return {
                'total_quizzes': total_quizzes,
                'average_score': 0,
                'best_score': 0,
                'worst_score': 0
            }
        
        average_score = sum(score_percentages) / len(score_percentages)
        best_score = max(score_percentages)
        worst_score = min(score_percentages)
        
        return {
            'total_quizzes': total_quizzes,
            'average_score': round(average_score, 1),
            'best_score': round(best_score, 1),
            'worst_score': round(worst_score, 1)
        }
    except Exception:
        return {
            'total_quizzes': total_quizzes,
            'average_score': 0,
            'best_score': 0,
            'worst_score': 0
        }

def get_subject_scores(user_scores):
    """Group scores by subject and calculate percentages"""
    subject_scores = {}
    for score in user_scores:
        subject = score.quiz.chapter.subject
        if subject.name not in subject_scores:
            subject_scores[subject.name] = []
        percentage = calculate_percentage(score.total_score, score.max_score)
        subject_scores[subject.name].append({
            'score': score,
            'percentage': percentage
        })
    
    return subject_scores

