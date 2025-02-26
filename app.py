from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.database import db, User, Admin, Subject, Chapter, Quiz, Question
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SECRET_KEY'] = 'hail-hydra'
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
        try:
            username = request.form['username']
            password = request.form['password']
            full_name = request.form['full_name']
            qualification = request.form['qualification']
            dob_str = request.form['dob']

            if not is_valid_email(username):
                flash('Please enter a valid email address')
                return render_template('register.html')

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                flash('Email already registered')
                return render_template('register.html')

            # Convert date string to datetime object
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format')
                return render_template('register.html')

            # Create new user
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                password=hashed_password,
                full_name=full_name,
                qualification=qualification,
                dob=dob
            )

            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred during registration: {str(e)}')
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
    subjects = Subject.query.all()
    users = User.query.all()
    return render_template('admin_dashboard.html', subjects=subjects, users=users)

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'user':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user)

@app.route('/admin/subjects', methods=['GET', 'POST'])
def manage_subjects():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
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

@app.route('/admin/subjects/<int:id>/edit', methods=['GET', 'POST'])
def edit_subject(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(id)
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form['description']
        try:
            db.session.commit()
            flash('Subject updated successfully!')
            return redirect(url_for('manage_subjects'))
        except:
            db.session.rollback()
            flash('Error updating subject. Please try again.')
    
    return render_template('admin/edit_subject.html', subject=subject)

@app.route('/admin/subjects/<int:id>/delete')
def delete_subject(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(id)
    try:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting subject. Please try again.')
    
    return redirect(url_for('manage_subjects'))

@app.route('/admin/subjects/<int:subject_id>/chapters', methods=['GET', 'POST'])
def manage_chapters(subject_id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
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

@app.route('/admin/chapters/<int:id>/edit', methods=['GET', 'POST'])
def edit_chapter(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    chapter = Chapter.query.get_or_404(id)
    if request.method == 'POST':
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        try:
            db.session.commit()
            flash('Chapter updated successfully!')
            return redirect(url_for('manage_chapters', subject_id=chapter.subject_id))
        except:
            db.session.rollback()
            flash('Error updating chapter. Please try again.')
    
    return render_template('admin/edit_chapter.html', chapter=chapter)

@app.route('/admin/chapters/<int:id>/delete')
def delete_chapter(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    chapter = Chapter.query.get_or_404(id)
    subject_id = chapter.subject_id
    try:
        db.session.delete(chapter)
        db.session.commit()
        flash('Chapter deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting chapter. Please try again.')
    
    return redirect(url_for('manage_chapters', subject_id=subject_id))

@app.route('/admin/chapters/<int:chapter_id>/quizzes', methods=['GET', 'POST'])
def manage_quizzes(chapter_id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
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

@app.route('/admin/quizzes/<int:id>/edit', methods=['GET', 'POST'])
def edit_quiz(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(id)
    if request.method == 'POST':
        quiz.date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        quiz.time_duration = request.form['time_duration']
        try:
            db.session.commit()
            flash('Quiz updated successfully!')
            return redirect(url_for('manage_quizzes', chapter_id=quiz.chapter_id))
        except:
            db.session.rollback()
            flash('Error updating quiz. Please try again.')
    
    return render_template('admin/edit_quiz.html', quiz=quiz)

@app.route('/admin/quizzes/<int:id>/delete')
def delete_quiz(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(id)
    chapter_id = quiz.chapter_id
    try:
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting quiz. Please try again.')
    
    return redirect(url_for('manage_quizzes', chapter_id=chapter_id))

@app.route('/admin/quizzes/<int:quiz_id>/questions', methods=['GET', 'POST'])
def manage_questions(quiz_id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
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

@app.route('/admin/questions/<int:id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
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
            return redirect(url_for('manage_questions', quiz_id=question.quiz_id))
        except:
            db.session.rollback()
            flash('Error updating question. Please try again.')
    
    return render_template('admin/edit_question.html', question=question)

@app.route('/admin/questions/<int:id>/delete')
def delete_question(id):
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    
    question = Question.query.get_or_404(id)
    quiz_id = question.quiz_id
    try:
        db.session.delete(question)
        db.session.commit()
        flash('Question deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting question. Please try again.')
    
    return redirect(url_for('manage_questions', quiz_id=quiz_id))

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
    create_admin() 
    app.run(debug=True)
