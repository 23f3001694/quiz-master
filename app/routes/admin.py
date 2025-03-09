from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.database import db, Subject, Chapter, Quiz, Question, User
from datetime import datetime
from functools import wraps
from sqlalchemy import or_

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@admin_required
def dashboard():
    subjects = Subject.query.all()
    users = User.query.all()
    return render_template('admin/dashboard.html', subjects=subjects, users=users)

@admin.route('/subjects', methods=['GET', 'POST'])
@admin_required
def manage_subjects():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        subject = Subject(name=name, description=description)
        try:
            db.session.add(subject)
            db.session.commit()
            flash('Subject created successfully!')
        except:
            db.session.rollback()
            flash('Error creating subject. Please try again.')
        
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@admin.route('/subjects/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form['description']
        try:
            db.session.commit()
            flash('Subject updated successfully!')
            return redirect(url_for('admin.manage_subjects'))
        except:
            db.session.rollback()
            flash('Error updating subject. Please try again.')
    
    return render_template('admin/edit_subject.html', subject=subject)

@admin.route('/subjects/<int:id>/delete')
@admin_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    try:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting subject. Please try again.')
    
    return redirect(url_for('admin.manage_subjects'))

@admin.route('/subjects/<int:subject_id>/chapters', methods=['GET', 'POST'])
@admin_required
def manage_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        chapter = Chapter(name=name, description=description, subject_id=subject_id)
        try:
            db.session.add(chapter)
            db.session.commit()
            flash('Chapter created successfully!')
        except:
            db.session.rollback()
            flash('Error creating chapter. Please try again.')
    
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template('admin/chapters.html', subject=subject, chapters=chapters)

@admin.route('/chapters/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    if request.method == 'POST':
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        try:
            db.session.commit()
            flash('Chapter updated successfully!')
            return redirect(url_for('admin.manage_chapters', subject_id=chapter.subject_id))
        except:
            db.session.rollback()
            flash('Error updating chapter. Please try again.')
    
    return render_template('admin/edit_chapter.html', chapter=chapter)

@admin.route('/chapters/<int:id>/delete')
@admin_required
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    subject_id = chapter.subject_id
    try:
        db.session.delete(chapter)
        db.session.commit()
        flash('Chapter deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting chapter. Please try again.')
    
    return redirect(url_for('admin.manage_chapters', subject_id=subject_id))

@admin.route('/chapters/<int:chapter_id>/quizzes', methods=['GET', 'POST'])
@admin_required
def manage_quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == 'POST':
        date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        time_duration = request.form['time_duration']
        
        quiz = Quiz(chapter_id=chapter_id, date_of_quiz=date_of_quiz, time_duration=time_duration)
        try:
            db.session.add(quiz)
            db.session.commit()
            flash('Quiz created successfully!')
        except:
            db.session.rollback()
            flash('Error creating quiz. Please try again.')
    
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('admin/quizzes.html', chapter=chapter, quizzes=quizzes)

@admin.route('/quizzes/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    if request.method == 'POST':
        quiz.date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        quiz.time_duration = request.form['time_duration']
        try:
            db.session.commit()
            flash('Quiz updated successfully!')
            return redirect(url_for('admin.manage_quizzes', chapter_id=quiz.chapter_id))
        except:
            db.session.rollback()
            flash('Error updating quiz. Please try again.')
    
    return render_template('admin/edit_quiz.html', quiz=quiz)

@admin.route('/quizzes/<int:id>/delete')
@admin_required
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    chapter_id = quiz.chapter_id
    try:
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting quiz. Please try again.')
    
    return redirect(url_for('admin.manage_quizzes', chapter_id=chapter_id))

@admin.route('/quizzes/<int:quiz_id>/questions', methods=['GET', 'POST'])
@admin_required
def manage_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        question = Question(
            quiz_id=quiz_id,
            question_statement=request.form['question_statement'],
            option1=request.form['option1'],
            option2=request.form['option2'],
            option3=request.form['option3'],
            option4=request.form['option4'],
            correct_option=int(request.form['correct_option'])
        )
        try:
            db.session.add(question)
            db.session.commit()
            flash('Question created successfully!')
        except:
            db.session.rollback()
            flash('Error creating question. Please try again.')
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('admin/questions.html', quiz=quiz, questions=questions)

@admin.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_question(id):
    question = Question.query.get_or_404(id)
    if request.method == 'POST':
        question.question_statement = request.form['question_statement']
        question.option1 = request.form['option1']
        question.option2 = request.form['option2']
        question.option3 = request.form['option3']
        question.option4 = request.form['option4']
        question.correct_option = int(request.form['correct_option'])
        try:
            db.session.commit()
            flash('Question updated successfully!')
            return redirect(url_for('admin.manage_questions', quiz_id=question.quiz_id))
        except:
            db.session.rollback()
            flash('Error updating question. Please try again.')
    
    return render_template('admin/edit_question.html', question=question)

@admin.route('/questions/<int:id>/delete')
@admin_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    quiz_id = question.quiz_id
    try:
        db.session.delete(question)
        db.session.commit()
        flash('Question deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting question. Please try again.')
    
    return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))

@admin.route('/users/<int:id>')
@admin_required
def view_user(id):
    user = User.query.get_or_404(id)
    return render_template('admin/view_user.html', user=user) 

@admin.route('/search', methods=['GET'])
@admin_required
def search():
    query = request.args.get('query', '').strip()
    search_type = request.args.get('type', 'all')
    
    if not query:
        flash('Please enter a search query', 'error')
        return redirect(request.referrer or url_for('admin.dashboard'))
        
    results = {}
    
    if search_type in ['all', 'users']:
        users = User.query.filter(
            or_(
                User.username.ilike(f'%{query}%'),
                User.email.ilike(f'%{query}%'),
                User.full_name.ilike(f'%{query}%')
            )
        ).all()
        results['users'] = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name
        } for user in users]
    
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
    
    if search_type in ['all', 'questions']:
        questions = Question.query.filter(
            Question.question_statement.ilike(f'%{query}%')
        ).all()
        results['questions'] = [{
            'id': question.id,
            'quiz_id': question.quiz_id,
            'statement': question.question_statement
        } for question in questions]
    
    if not any(results.values()):
        flash('No results found for your search', 'info')
        return redirect(request.referrer or url_for('admin.dashboard'))
        
    return render_template('admin/search_results.html', results=results, query=query)
