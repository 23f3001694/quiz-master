from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    """
    User model representing a student/quiz taker in the system.
    
    Attributes:
        id (int): Primary key for the user
        username (str): Unique username for the user
        email (str): Unique email address
        password (str): Hashed password
        full_name (str): User's full name
        qualification (str): User's educational qualification
        dob (Date): User's date of birth
        scores (relationship): One-to-many relationship with Score model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    scores = db.relationship('Score', backref='user', lazy=True)

# Admin model
class Admin(db.Model):
    """
    Admin model representing system administrators.
    
    Attributes:
        id (int): Primary key for the admin
        username (str): Unique username for the admin
        email (str): Unique email address
        password (str): Hashed password
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Subject model
class Subject(db.Model):
    """
    Subject model representing a course subject.
    
    Attributes:
        id (int): Primary key for the subject
        name (str): Unique name of the subject
        description (str): Detailed description of the subject
        chapters (relationship): One-to-many relationship with Chapter model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')

# Chapter model
class Chapter(db.Model):
    """
    Chapter model representing a subject chapter.
    
    Attributes:
        id (int): Primary key for the chapter
        subject_id (int): Foreign key referencing Subject model
        name (str): Name of the chapter
        description (str): Detailed description of the chapter
        quizzes (relationship): One-to-many relationship with Quiz model
    """
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')

# Quiz model
class Quiz(db.Model):
    """
    Quiz model representing an assessment for a chapter.
    
    Attributes:
        id (int): Primary key for the quiz
        chapter_id (int): Foreign key referencing Chapter model
        date_of_quiz (DateTime): Date when the quiz is scheduled
        start_time (Time): Quiz start time
        end_time (Time): Quiz end time
        time_duration (int): Duration of the quiz in minutes
        questions (relationship): One-to-many relationship with Question model
        scores (relationship): One-to-many relationship with Score model
    """
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade='all, delete-orphan')

# Question model
class Question(db.Model):
    """
    Question model representing a quiz question.
    
    Attributes:
        id (int): Primary key for the question
        quiz_id (int): Foreign key referencing Quiz model
        question_statement (str): The actual question text
        option1 (str): First answer option
        option2 (str): Second answer option
        option3 (str): Third answer option
        option4 (str): Fourth answer option
        correct_option (int): Integer indicating the correct option (1-4)
    """
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

# Score model
class Score(db.Model):
    """
    Score model representing a user's quiz performance.
    
    Attributes:
        id (int): Primary key for the score
        quiz_id (int): Foreign key referencing Quiz model
        user_id (int): Foreign key referencing User model
        total_score (int): Score achieved by the user
        max_score (int): Maximum possible score for the quiz
    """
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")
