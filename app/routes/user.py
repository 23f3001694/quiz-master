from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash
from app.models.database import User, Subject, Chapter, Quiz, Question, Score, db
from functools import wraps
from datetime import datetime
from sqlalchemy import or_

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
    user_scores = Score.query.filter_by(user_id=session['user_id']).all()
    attempted_quiz_ids = {score.quiz_id for score in user_scores}
    return render_template('user/subject_detail.html', 
                         subject=subject, 
                         attempted_quiz_ids=attempted_quiz_ids)

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
    
    existing_score = Score.query.filter_by(user_id=session['user_id'], quiz_id=quiz_id).first()
    if existing_score:
        flash('You have already attempted this quiz.')
        return redirect(url_for('user.quiz_detail', quiz_id=quiz_id))
    
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
            total_score=score,
            max_score=total_questions
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

@user.route('/quiz-summary')
@user_required
def quiz_summary():
    user_scores = Score.query.filter_by(user_id=session['user_id']).all()
    
    total_quizzes = len(user_scores)
    if total_quizzes > 0:
        score_percentages = [(score.total_score / score.max_score * 100) for score in user_scores]
        average_score = sum(score_percentages) / len(score_percentages)
        best_score = max(score_percentages)
        worst_score = min(score_percentages)
    else:
        average_score = best_score = worst_score = 0
    
    subject_scores = {}
    for score in user_scores:
        subject = score.quiz.chapter.subject
        if subject.name not in subject_scores:
            subject_scores[subject.name] = []
        percentage = (score.total_score / score.max_score * 100)
        subject_scores[subject.name].append({
            'score': score,
            'percentage': percentage
        })
    
    return render_template('user/quiz_summary.html', 
                         user_scores=user_scores,
                         total_quizzes=total_quizzes,
                         average_score=round(average_score, 1),
                         best_score=round(best_score, 1),
                         worst_score=round(worst_score, 1),
                         subject_scores=subject_scores) 

@user.route('/search', methods=['GET'])
@user_required
def search():
    query = request.args.get('query', '').strip()
    search_type = request.args.get('type', 'all')
    
    if not query:
        flash('Please enter a search query', 'error')
        return redirect(request.referrer or url_for('user.dashboard'))
        
    results = {}
    
    if search_type in ['all', 'subjects']:
        subjects = Subject.query.filter(
            or_(
                Subject.name.ilike(f'%{query}%'),
                Subject.description.ilike(f'%{query}%')
            )
        ).all()
        results['subjects'] = [{
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        } for subject in subjects]
    
    if search_type in ['all', 'quizzes']:
        quizzes = Quiz.query.join(Chapter).filter(
            or_(
                Chapter.name.ilike(f'%{query}%'),
                Quiz.time_duration.ilike(f'%{query}%')
            )
        ).all()
        results['quizzes'] = [{
            'id': quiz.id,
            'chapter': quiz.chapter.name,
            'date': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': quiz.time_duration
        } for quiz in quizzes]
    
    if not any(results.values()):
        flash('No results found for your search', 'info')
        return redirect(request.referrer or url_for('user.dashboard'))
        
    return render_template('user/search_results.html', results=results, query=query) 