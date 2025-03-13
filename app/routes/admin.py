from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.database import db, Subject, Chapter, Quiz, Question, User
from datetime import datetime
from app.utils.helpers import admin_required, search_users, search_subjects, search_chapters, search_quizzes, search_questions
from app.utils.chart_utils import generate_admin_quiz_stats, generate_admin_user_stats

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@admin_required
def dashboard():
    """
    Render the admin dashboard page.
    
    Displays an overview of all subjects and users in the system,
    along with user statistics visualization.
    
    Returns:
        rendered template: The admin dashboard page with subjects, users and stats
    """
    subjects = Subject.query.all()
    users = User.query.all()
    
    user_stats_chart = generate_admin_user_stats(users)
    
    return render_template('admin/dashboard.html', 
                         subjects=subjects, 
                         users=users,
                         user_stats_chart=user_stats_chart)

@admin.route('/subjects', methods=['GET'])
@admin_required
def manage_subjects():
    """
    Display the subject management page.
    
    Lists all subjects in the system for administrative operations.
    
    Returns:
        rendered template: The subject management page with list of all subjects
    """
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@admin.route('/subjects/add', methods=['GET', 'POST'])
@admin_required
def add_subject():
    """
    Handle subject creation.
    
    GET: Display the subject creation form
    POST: Process the subject creation request
    
    Returns:
        GET: rendered template with the subject creation form
        POST: redirect to the subject management page on success,
              or back to form with error message on failure
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        subject = Subject(name=name, description=description)
        try:
            db.session.add(subject)
            db.session.commit()
            flash('Subject created successfully!')
            return redirect(url_for('admin.manage_subjects'))
        except:
            db.session.rollback()
            flash('Error creating subject. Please try again.')
    
    return render_template('admin/add_subject.html')

@admin.route('/subjects/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_subject(id):
    """
    Handle subject editing.
    
    GET: Display the subject edit form
    POST: Process the subject update request
    
    Args:
        id (int): The ID of the subject to edit
        
    Returns:
        GET: rendered template with the subject edit form
        POST: redirect to subject management page on success,
              or back to form with error message on failure
    """
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
    """
    Delete a subject from the system.
    
    Args:
        id (int): The ID of the subject to delete
        
    Returns:
        redirect: Redirects to subject management page with success/error message
    """
    subject = Subject.query.get_or_404(id)
    try:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting subject: {str(e)}")  # For server logs
        flash(f'Error deleting subject: {str(e)}')
    
    return redirect(url_for('admin.manage_subjects'))

@admin.route('/subjects/<int:subject_id>/chapters', methods=['GET'])
@admin_required
def manage_chapters(subject_id):
    """
    Display the chapter management page for a specific subject.
    
    Args:
        subject_id (int): The ID of the subject whose chapters to manage
        
    Returns:
        rendered template: The chapter management page with list of chapters
                         for the specified subject
    """
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template('admin/chapters.html', subject=subject, chapters=chapters)

@admin.route('/subjects/<int:subject_id>/chapters/add', methods=['GET', 'POST'])
@admin_required
def add_chapter(subject_id):
    """
    Handle chapter creation for a specific subject.
    
    GET: Display the chapter creation form
    POST: Process the chapter creation request
    
    Args:
        subject_id (int): The ID of the subject to add chapter to
        
    Returns:
        GET: rendered template with the chapter creation form
        POST: redirect to chapter management page on success,
              or back to form with error message on failure
    """
    subject = Subject.query.get_or_404(subject_id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        chapter = Chapter(name=name, description=description, subject_id=subject_id)
        try:
            db.session.add(chapter)
            db.session.commit()
            flash('Chapter created successfully!')
            return redirect(url_for('admin.manage_chapters', subject_id=subject_id))
        except:
            db.session.rollback()
            flash('Error creating chapter. Please try again.')
    
    return render_template('admin/add_chapter.html', subject=subject)

@admin.route('/chapters/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_chapter(id):
    """
    Handle chapter editing.
    
    GET: Display the chapter edit form
    POST: Process the chapter update request
    
    Args:
        id (int): The ID of the chapter to edit
        
    Returns:
        GET: rendered template with the chapter edit form and associated quizzes
        POST: redirect to chapter management page on success,
              or back to form with error message on failure
    """
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
    
    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
    return render_template('admin/edit_chapter.html', chapter=chapter, quizzes=quizzes)

@admin.route('/chapters/<int:id>/delete')
@admin_required
def delete_chapter(id):
    """
    Delete a chapter from the system.
    
    Args:
        id (int): The ID of the chapter to delete
        
    Returns:
        redirect: Redirects to chapter management page with success/error message
    """
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

@admin.route('/chapters/<int:chapter_id>/quizzes', methods=['GET'])
@admin_required
def manage_quizzes(chapter_id):
    """
    Display the quiz management page for a specific chapter.
    
    Shows all quizzes for the chapter along with quiz statistics visualization.
    
    Args:
        chapter_id (int): The ID of the chapter whose quizzes to manage
        
    Returns:
        rendered template: The quiz management page with list of quizzes
                         and statistics for the specified chapter
    """
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    quiz_stats_chart = generate_admin_quiz_stats(quizzes)
    
    return render_template('admin/quizzes.html', 
                         chapter=chapter, 
                         quizzes=quizzes,
                         quiz_stats_chart=quiz_stats_chart)

@admin.route('/chapters/<int:chapter_id>/quizzes/add', methods=['GET', 'POST'])
@admin_required
def add_quiz(chapter_id):
    """
    Handle quiz creation for a specific chapter.
    
    GET: Display the quiz creation form
    POST: Process the quiz creation request
    
    Args:
        chapter_id (int): The ID of the chapter to add quiz to
        
    Returns:
        GET: rendered template with the quiz creation form
        POST: redirect to quiz management page on success,
              or back to form with error message on failure
    """
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == 'POST':
        date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        time_duration = request.form['time_duration']
        
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']
        
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
        
        try:
            time_duration = int(time_duration)
            if time_duration <= 0:
                flash('Duration must be a positive number', 'error')
                return redirect(url_for('admin.add_quiz', chapter_id=chapter_id))
        except ValueError:
            flash('Duration must be a valid number', 'error')
            return redirect(url_for('admin.add_quiz', chapter_id=chapter_id))
        
        quiz = Quiz(
            chapter_id=chapter_id, 
            date_of_quiz=date_of_quiz, 
            time_duration=time_duration,
            start_time=start_time,
            end_time=end_time
        )
        try:
            db.session.add(quiz)
            db.session.commit()
            flash('Quiz created successfully!')
            return redirect(url_for('admin.manage_quizzes', chapter_id=chapter_id))
        except:
            db.session.rollback()
            flash('Error creating quiz. Please try again.')
    
    return render_template('admin/add_quiz.html', chapter=chapter)

@admin.route('/quizzes/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_quiz(id):
    """
    Handle quiz editing.
    
    GET: Display the quiz edit form
    POST: Process the quiz update request
    
    Args:
        id (int): The ID of the quiz to edit
        
    Returns:
        GET: rendered template with the quiz edit form
        POST: redirect to quiz management page on success,
              or back to form with error message on failure
    """
    quiz = Quiz.query.get_or_404(id)
    if request.method == 'POST':
        quiz.date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        time_duration = request.form['time_duration']
        
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']
        
        quiz.start_time = datetime.strptime(start_time_str, '%H:%M').time()
        quiz.end_time = datetime.strptime(end_time_str, '%H:%M').time()
        
        try:
            time_duration = int(time_duration)
            if time_duration <= 0:
                flash('Duration must be a positive number', 'error')
                return redirect(url_for('admin.edit_quiz', quiz_id=id))
            quiz.time_duration = time_duration
            db.session.commit()
            flash('Quiz updated successfully!')
            return redirect(url_for('admin.manage_quizzes', chapter_id=quiz.chapter_id))
        except ValueError:
            flash('Duration must be a valid number', 'error')
            return redirect(url_for('admin.edit_quiz', quiz_id=id))
    
    return render_template('admin/edit_quiz.html', quiz=quiz)

@admin.route('/quizzes/<int:id>/delete')
@admin_required
def delete_quiz(id):
    """
    Delete a quiz from the system.
    
    Args:
        id (int): The ID of the quiz to delete
        
    Returns:
        redirect: Redirects to quiz management page with success/error message
    """
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

@admin.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
@admin_required
def manage_questions(quiz_id):
    """
    Display the question management page for a specific quiz.
    
    Args:
        quiz_id (int): The ID of the quiz whose questions to manage
        
    Returns:
        rendered template: The question management page with list of questions
                         for the specified quiz
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('admin/questions.html', quiz=quiz, questions=questions)

@admin.route('/quizzes/<int:quiz_id>/questions/add', methods=['GET', 'POST'])
@admin_required
def add_question(quiz_id):
    """
    Handle question creation for a specific quiz.
    
    GET: Display the question creation form
    POST: Process the question creation request
    
    Args:
        quiz_id (int): The ID of the quiz to add question to
        
    Returns:
        GET: rendered template with the question creation form
        POST: redirect to question management page on success,
              or back to form with error message on failure
    """
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
            return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))
        except:
            db.session.rollback()
            flash('Error creating question. Please try again.')
    
    return render_template('admin/add_question.html', quiz=quiz)

@admin.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_question(id):
    """
    Handle question editing.
    
    GET: Display the question edit form
    POST: Process the question update request
    
    Args:
        id (int): The ID of the question to edit
        
    Returns:
        GET: rendered template with the question edit form
        POST: redirect to question management page on success,
              or back to form with error message on failure
    """
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
    """
    Delete a question from the system.
    
    Args:
        id (int): The ID of the question to delete
        
    Returns:
        redirect: Redirects to question management page with success/error message
    """
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

@admin.route('/users')
@admin_required
def manage_users():
    """
    Display the user management page.
    
    Lists all users in the system for administrative operations.
    
    Returns:
        rendered template: The user management page with list of all users
    """
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:id>')
@admin_required
def view_user(id):
    """
    Display detailed information about a specific user.
    
    Args:
        id (int): The ID of the user to view
        
    Returns:
        rendered template: The user detail page with user information
    """
    user = User.query.get_or_404(id)
    return render_template('admin/view_user.html', user=user)

@admin.route('/users/<int:id>/delete')
@admin_required
def delete_user(id):
    """
    Delete a user from the system.
    
    Prevents deletion of the currently logged-in user.
    
    Args:
        id (int): The ID of the user to delete
        
    Returns:
        redirect: Redirects to user management page with success/error message
    """
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('Error deleting user. Please try again.', 'danger')
    
    return redirect(url_for('admin.manage_users'))

@admin.route('/search', methods=['GET'])
@admin_required
def search():
    """
    Handle global search across all entities in the system.
    
    Performs search based on query and type parameters, searching across
    users, subjects, chapters, quizzes, and questions as specified.
    
    Query Parameters:
        query (str): The search term to look for
        type (str): The type of entities to search for ('all', 'users',
                   'subjects', 'chapters', 'quizzes', 'questions')
    
    Returns:
        rendered template: Search results page showing matching entities,
                         or redirect to dashboard if no results found
    """
    query = request.args.get('query', '').strip()
    search_type = request.args.get('type', 'all')
    
    if not query:
        flash('Please enter a search query', 'error')
        return redirect(request.referrer or url_for('admin.dashboard'))
        
    results = {}
    
    if search_type in ['all', 'users']:
        users = search_users(query)
        results['users'] = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name
        } for user in users]
    
    if search_type in ['all', 'subjects']:
        subjects = search_subjects(query)
        results['subjects'] = [{
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        } for subject in subjects]
    
    if search_type in ['all', 'chapters']:
        chapters = search_chapters(query)
        results['chapters'] = [{
            'id': chapter.id,
            'name': chapter.name,
            'subject_name': chapter.subject.name,
            'subject_id': chapter.subject_id
        } for chapter in chapters]
    
    if search_type in ['all', 'quizzes']:
        quizzes = search_quizzes(query)
        results['quizzes'] = [{
            'id': quiz.id,
            'chapter': quiz.chapter.name,
            'chapter_id': quiz.chapter_id,
            'date': quiz.date_of_quiz.strftime('%Y-%m-%d'),
            'start_time': quiz.start_time.strftime('%H:%M'),
            'end_time': quiz.end_time.strftime('%H:%M'),
            'duration': quiz.time_duration
        } for quiz in quizzes]
    
    if search_type in ['all', 'questions']:
        questions = search_questions(query)
        results['questions'] = [{
            'id': question.id,
            'quiz_id': question.quiz_id,
            'statement': question.question_statement[:50] + '...' if len(question.question_statement) > 50 else question.question_statement
        } for question in questions]
    
    if not any(results.values()):
        flash('No results found for your search', 'info')
        return redirect(request.referrer or url_for('admin.dashboard'))
    
    return render_template('admin/search_results.html', results=results, query=query)
