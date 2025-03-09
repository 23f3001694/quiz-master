from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.models.database import User, Subject, Chapter, Quiz, Question, Score, db
from functools import wraps
from datetime import datetime

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
    subjects = Subject.query.all()
    return render_template('user/dashboard.html', user=user, subjects=subjects)

@user.route('/subject/<int:subject_id>')
@user_required
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('user/subject_detail.html', subject=subject)

@user.route('/quiz/<int:quiz_id>')
@user_required
def quiz_detail(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    existing_score = Score.query.filter_by(user_id=session['user_id'], quiz_id=quiz_id).first()
    return render_template('user/quiz_detail.html', quiz=quiz, existing_score=existing_score)

@user.route('/quiz/<int:quiz_id>/attempt', methods=['GET', 'POST'])
@user_required
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        score = 0
        total_questions = len(quiz.questions)
        
        for question in quiz.questions:
            selected_answer = request.form.get(f'question_{question.id}')
            if selected_answer and int(selected_answer) == question.correct_option:
                score += 1
        
        new_score = Score(
            quiz_id=quiz_id,
            user_id=session['user_id'],
            total_score=score
        )
        db.session.add(new_score)
        db.session.commit()
        
        return redirect(url_for('user.quiz_result', quiz_id=quiz_id, score_id=new_score.id))
    
    return render_template('user/attempt_quiz.html', quiz=quiz)

@user.route('/quiz/<int:quiz_id>/result/<int:score_id>')
@user_required
def quiz_result(quiz_id, score_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    score = Score.query.get_or_404(score_id)
    return render_template('user/quiz_result.html', quiz=quiz, score=score) 