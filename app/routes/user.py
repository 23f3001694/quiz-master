from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash
from app.models.database import User, Subject, Chapter, Quiz, Question, Score, db
from app.utils.helpers import user_required, is_quiz_available, search_subjects, search_quizzes, format_datetime, calculate_score_statistics, get_subject_scores, calculate_percentage
from app.utils.chart_utils import generate_user_performance_chart, generate_subject_performance_chart
from datetime import datetime
from sqlalchemy import or_

user = Blueprint('user', __name__, url_prefix='/user')

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
    
    # Check if the quiz is within the valid timeframe
    is_available = is_quiz_available(quiz)
    
    return render_template('user/quiz_detail.html', 
                         quiz=quiz, 
                         existing_score=existing_score,
                         is_available=is_available)

@user.route('/quiz/<int:quiz_id>/attempt', methods=['GET', 'POST'])
@user_required
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Check if the quiz is within the valid timeframe
    if not is_quiz_available(quiz):
        flash('This quiz is not available at this time.', 'danger')
        return redirect(url_for('user.quiz_detail', quiz_id=quiz_id))
    
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
    percentage = calculate_percentage(score.total_score, score.max_score)
    return render_template('user/quiz_result.html', quiz=quiz, score=score, percentage=percentage) 

@user.route('/quiz-summary')
@user_required
def quiz_summary():
    user_scores = Score.query.filter_by(user_id=session['user_id']).all()
    
    stats = calculate_score_statistics(user_scores)
    subject_scores = get_subject_scores(user_scores)
    
    # Generate performance charts
    performance_chart = generate_user_performance_chart(user_scores)
    subject_chart = generate_subject_performance_chart(subject_scores)
    
    return render_template('user/quiz_summary.html', 
                         user_scores=user_scores,
                         total_quizzes=stats['total_quizzes'],
                         average_score=stats['average_score'],
                         best_score=stats['best_score'],
                         worst_score=stats['worst_score'],
                         subject_scores=subject_scores,
                         performance_chart=performance_chart,
                         subject_chart=subject_chart) 

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
        subjects = search_subjects(query)
        results['subjects'] = [{
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        } for subject in subjects]
    
    if search_type in ['all', 'quizzes']:
        quizzes = search_quizzes(query)
        results['quizzes'] = [{
            'id': quiz.id,
            'chapter': quiz.chapter.name,
            'chapter_id': quiz.chapter_id,
            'date': format_datetime(quiz.date_of_quiz),
            'duration': quiz.time_duration,
            'is_available': is_quiz_available(quiz)
        } for quiz in quizzes]
    
    if not any(results.values()):
        flash('No results found for your search', 'info')
        return redirect(request.referrer or url_for('user.dashboard'))
    
    return render_template('user/search_results.html', results=results, query=query) 