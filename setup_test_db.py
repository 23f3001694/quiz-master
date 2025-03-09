from app import create_app
from app.models.database import db, Admin, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime, time, timedelta
from werkzeug.security import generate_password_hash

def setup_test_db():
    """
    Set up a new database with test data including quizzes with different time settings
    """
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin exists
        admin = Admin.query.filter_by(username="admin").first()
        if not admin:
            admin = Admin(
                username="admin",
                email="admin@example.com",
                password=generate_password_hash("password")
            )
            db.session.add(admin)
        
        # Check if test user exists
        user = User.query.filter_by(username="testuser").first()
        if not user:
            user = User(
                username="testuser",
                email="test@example.com",
                password=generate_password_hash("password"),
                full_name="Test User",
                qualification="Student",
                dob=datetime(2000, 1, 1)
            )
            db.session.add(user)
        
        db.session.commit()
        
        # Create subjects
        math = Subject.query.filter_by(name="Mathematics").first()
        if not math:
            math = Subject(name="Mathematics", description="Study of numbers, quantities, and shapes")
            db.session.add(math)
        
        science = Subject.query.filter_by(name="Science").first()
        if not science:
            science = Subject(name="Science", description="Study of the natural world")
            db.session.add(science)
        
        db.session.commit()
        
        # Create chapters
        algebra = Chapter.query.filter_by(name="Algebra").first()
        if not algebra:
            algebra = Chapter(subject_id=math.id, name="Algebra", description="Study of mathematical symbols and rules")
            db.session.add(algebra)
        
        geometry = Chapter.query.filter_by(name="Geometry").first()
        if not geometry:
            geometry = Chapter(subject_id=math.id, name="Geometry", description="Study of shapes and spaces")
            db.session.add(geometry)
        
        physics = Chapter.query.filter_by(name="Physics").first()
        if not physics:
            physics = Chapter(subject_id=science.id, name="Physics", description="Study of matter, energy, and their interactions")
            db.session.add(physics)
        
        chemistry = Chapter.query.filter_by(name="Chemistry").first()
        if not chemistry:
            chemistry = Chapter(subject_id=science.id, name="Chemistry", description="Study of substances and their properties")
            db.session.add(chemistry)
        
        db.session.commit()
        
        # Delete existing quizzes to avoid conflicts
        Quiz.query.delete()
        db.session.commit()
        
        # Get current date and time
        now = datetime.now()
        today = now.date()
        current_time = now.time()
        
        # Create quizzes with different time settings
        
        # Quiz 1: Available now (current date, current time + 1 hour)
        quiz1 = Quiz(
            chapter_id=algebra.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time(current_time.hour, 0),
            end_time=time((current_time.hour + 1) % 24, 0),
            time_duration="60 mins"
        )
        
        # Quiz 2: Available later today
        quiz2 = Quiz(
            chapter_id=geometry.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time((current_time.hour + 2) % 24, 0),
            end_time=time((current_time.hour + 3) % 24, 0),
            time_duration="60 mins"
        )
        
        # Quiz 3: Available tomorrow
        tomorrow = today + timedelta(days=1)
        quiz3 = Quiz(
            chapter_id=physics.id,
            date_of_quiz=datetime.combine(tomorrow, time(0, 0)),
            start_time=time(10, 0),
            end_time=time(12, 0),
            time_duration="120 mins"
        )
        
        # Quiz 4: Available yesterday (expired)
        yesterday = today - timedelta(days=1)
        quiz4 = Quiz(
            chapter_id=chemistry.id,
            date_of_quiz=datetime.combine(yesterday, time(0, 0)),
            start_time=time(14, 0),
            end_time=time(16, 0),
            time_duration="120 mins"
        )
        
        db.session.add(quiz1)
        db.session.add(quiz2)
        db.session.add(quiz3)
        db.session.add(quiz4)
        db.session.commit()
        
        # Add questions to quizzes
        questions1 = [
            Question(
                quiz_id=quiz1.id,
                question_statement="What is the value of x in the equation 2x + 5 = 15?",
                option1="5",
                option2="10",
                option3="7.5",
                option4="4",
                correct_option=1
            ),
            Question(
                quiz_id=quiz1.id,
                question_statement="Solve for y: 3y - 6 = 12",
                option1="4",
                option2="6",
                option3="8",
                option4="10",
                correct_option=2
            ),
            Question(
                quiz_id=quiz1.id,
                question_statement="If f(x) = 2x² + 3x - 5, what is f(2)?",
                option1="9",
                option2="11",
                option3="13",
                option4="15",
                correct_option=2
            )
        ]
        
        questions2 = [
            Question(
                quiz_id=quiz2.id,
                question_statement="What is the area of a circle with radius 5 units?",
                option1="25π square units",
                option2="10π square units",
                option3="5π square units",
                option4="15π square units",
                correct_option=1
            ),
            Question(
                quiz_id=quiz2.id,
                question_statement="What is the sum of angles in a triangle?",
                option1="90 degrees",
                option2="180 degrees",
                option3="270 degrees",
                option4="360 degrees",
                correct_option=2
            )
        ]
        
        questions3 = [
            Question(
                quiz_id=quiz3.id,
                question_statement="What is Newton's First Law of Motion?",
                option1="F = ma",
                option2="An object at rest stays at rest unless acted upon by an external force",
                option3="For every action, there is an equal and opposite reaction",
                option4="Energy cannot be created or destroyed",
                correct_option=2
            ),
            Question(
                quiz_id=quiz3.id,
                question_statement="What is the unit of force in the SI system?",
                option1="Watt",
                option2="Joule",
                option3="Newton",
                option4="Pascal",
                correct_option=3
            )
        ]
        
        questions4 = [
            Question(
                quiz_id=quiz4.id,
                question_statement="What is the chemical symbol for gold?",
                option1="Go",
                option2="Gd",
                option3="Au",
                option4="Ag",
                correct_option=3
            ),
            Question(
                quiz_id=quiz4.id,
                question_statement="What is the pH of a neutral solution?",
                option1="0",
                option2="7",
                option3="10",
                option4="14",
                correct_option=2
            )
        ]
        
        for q in questions1 + questions2 + questions3 + questions4:
            db.session.add(q)
        
        db.session.commit()
        
        print("Database setup complete!")
        print(f"Current time: {now}")
        print(f"Quiz 1 (Available now): {today} from {quiz1.start_time} to {quiz1.end_time}")
        print(f"Quiz 2 (Available later today): {today} from {quiz2.start_time} to {quiz2.end_time}")
        print(f"Quiz 3 (Available tomorrow): {tomorrow} from {quiz3.start_time} to {quiz3.end_time}")
        print(f"Quiz 4 (Expired): {yesterday} from {quiz4.start_time} to {quiz4.end_time}")
        print("\nLogin credentials:")
        print("Admin - Username: admin, Password: password")
        print("User - Username: testuser, Password: password")

if __name__ == "__main__":
    setup_test_db() 