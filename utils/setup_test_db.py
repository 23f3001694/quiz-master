import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        
        user2 = User.query.filter_by(username="testuser2").first()
        if not user2:
            user2 = User(
                username="testuser2",
                email="test2@example.com",
                password=generate_password_hash("password"),
                full_name="Test User 2",    
                qualification="Student",
                dob=datetime(2000, 1, 1)
            )
            db.session.add(user2)
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

        english = Subject.query.filter_by(name="English").first()
        if not english:
            english = Subject(name="English", description="Study of the English language")
            db.session.add(english)
        
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
        
        nouns = Chapter.query.filter_by(name="Nouns").first()
        if not nouns:
            nouns = Chapter(subject_id=english.id, name="Nouns", description="Study of nouns")
            db.session.add(nouns)
        
        verbs = Chapter.query.filter_by(name="Verbs").first()   
        if not verbs:
            verbs = Chapter(subject_id=english.id, name="Verbs", description="Study of verbs")
            db.session.add(verbs)
        
        adjectives = Chapter.query.filter_by(name="Adjectives").first()
        if not adjectives:
            adjectives = Chapter(subject_id=english.id, name="Adjectives", description="Study of adjectives")
            db.session.add(adjectives)
        
            
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
            time_duration=60
        )


        # Quiz 2: Available later today
        quiz2 = Quiz(
            chapter_id=geometry.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time((current_time.hour + 2) % 24, 0),
            end_time=time((current_time.hour + 3) % 24, 0),
            time_duration=60
        )
        
        # Quiz 3: Available tomorrow
        tomorrow = today + timedelta(days=1)
        quiz3 = Quiz(
            chapter_id=physics.id,
            date_of_quiz=datetime.combine(tomorrow, time(0, 0)),
            start_time=time(10, 0),
            end_time=time(12, 0),
            time_duration=120
        )
        
        # Quiz 4: Available yesterday (expired)
        yesterday = today - timedelta(days=1)
        quiz4 = Quiz(
            chapter_id=chemistry.id,
            date_of_quiz=datetime.combine(yesterday, time(0, 0)),
            start_time=time(14, 0),
            end_time=time(16, 0),
            time_duration=120
        )

        # Quiz 5: Available now (current date, current time + 1 hour) for Science - Physics
        quiz5 = Quiz(
            chapter_id=physics.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time(current_time.hour, 0),
            end_time=time((current_time.hour + 1) % 24, 0),
            time_duration=60
        )
        
        # Quiz 6: Available now (current date, current time + 1 hour) for Science - Chemistry
        quiz6 = Quiz(
            chapter_id=chemistry.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time(current_time.hour, 0),
            end_time=time((current_time.hour + 1) % 24, 0),
            time_duration=60
        )

        # Quiz 7: Available later today for Mathematics - Algebra
        quiz7 = Quiz(
            chapter_id=algebra.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time((current_time.hour + 4) % 24, 0),
            end_time=time((current_time.hour + 5) % 24, 0),
            time_duration=60
        )

        # Quiz 8: Available tomorrow for Mathematics - Geometry
        quiz8 = Quiz(
            chapter_id=geometry.id,
            date_of_quiz=datetime.combine(tomorrow, time(0, 0)),
            start_time=time(14, 0),
            end_time=time(16, 0),
            time_duration=120
        )

        # Quiz 9: Available tomorrow for Science - Chemistry
        quiz9 = Quiz(
            chapter_id=chemistry.id,
            date_of_quiz=datetime.combine(tomorrow, time(0, 0)),
            start_time=time(16, 0),
            end_time=time(18, 0),
            time_duration=120
        )

        # Quiz 10: Expired (2 days ago) for Mathematics - Algebra
        two_days_ago = today - timedelta(days=2)
        quiz10 = Quiz(
            chapter_id=algebra.id,
            date_of_quiz=datetime.combine(two_days_ago, time(0, 0)),
            start_time=time(10, 0),
            end_time=time(12, 0),
            time_duration=120
        )

        # Quiz 11: Expired (3 days ago) for Science - Physics
        three_days_ago = today - timedelta(days=3)
        quiz11 = Quiz(
            chapter_id=physics.id,
            date_of_quiz=datetime.combine(three_days_ago, time(0, 0)),
            start_time=time(15, 0),
            end_time=time(17, 0),
            time_duration=120
        )

        # Quiz 12: Available now (current date, current time + 1 hour) for English - Nouns
        quiz12 = Quiz(
            chapter_id=nouns.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time(current_time.hour, 0),
            end_time=time((current_time.hour + 1) % 24, 0),
            time_duration=60
        )

        # Quiz 13: Available now (current date, current time + 1 hour) for English - Verbs
        quiz13 = Quiz(
            chapter_id=verbs.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),   
            start_time=time(current_time.hour, 0),
            end_time=time((current_time.hour + 1) % 24, 0),
            time_duration=60
        )
        
        # Quiz 14: Available later today for English - Adjectives
        quiz14 = Quiz(
            chapter_id=adjectives.id,
            date_of_quiz=datetime.combine(today, time(0, 0)),
            start_time=time((current_time.hour + 2) % 24, 0),
            end_time=time((current_time.hour + 3) % 24, 0), 
            time_duration=60
        )
        
        # Quiz 15: Available tomorrow for English - Nouns
        quiz15 = Quiz(
            chapter_id=nouns.id,
            date_of_quiz=datetime.combine(tomorrow, time(0, 0)),
            start_time=time(14, 0),
            end_time=time(16, 0),   
            time_duration=120
        )
        
        # Quiz 16: Available yesterday for English - Adjectives
        quiz16 = Quiz(
            chapter_id=adjectives.id,
            date_of_quiz=datetime.combine(yesterday, time(0, 0)),
            start_time=time(10, 0),
            end_time=time(12, 0),
            time_duration=120
        )
        
        
        
        
        db.session.add(quiz1)
        db.session.add(quiz2)
        db.session.add(quiz3)
        db.session.add(quiz4)
        db.session.add(quiz5)
        db.session.add(quiz6)
        db.session.add(quiz7)
        db.session.add(quiz8)
        db.session.add(quiz9)
        db.session.add(quiz10)
        db.session.add(quiz11)
        db.session.add(quiz12)
        db.session.add(quiz13)
        db.session.add(quiz14)
        db.session.add(quiz15)
        db.session.add(quiz16)
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
        
        questions5 = [
            Question(
                quiz_id=quiz5.id,
                question_statement="What is the speed of light in a vacuum?",
                option1="3 x 10^8 m/s",
                option2="3 x 10^6 m/s",
                option3="3 x 10^5 m/s",
                option4="3 x 10^7 m/s",
                correct_option=1
            ),
            Question(
                quiz_id=quiz5.id,
                question_statement="What is the formula for kinetic energy?",
                option1="KE = mv^2",
                option2="KE = 1/2 mv^2",
                option3="KE = 1/2 mv",
                option4="KE = mv",
                correct_option=2
            )
        ]
        
        questions6 = [
            Question(
                quiz_id=quiz6.id,
                question_statement="What is the atomic number of carbon?",
                option1="6",
                option2="12",
                option3="14",
                option4="16",
                correct_option=1
            ),
            Question(
                quiz_id=quiz6.id,
                question_statement="What is the chemical formula for water?",
                option1="H2O",
                option2="CO2",
                option3="O2",
                option4="H2",
                correct_option=1
            )
        ]
        
        # Questions for Quiz 7 (Advanced Algebra)
        questions7 = [
            Question(
                quiz_id=quiz7.id,
                question_statement="What is the solution to the quadratic equation x² - 4x + 4 = 0?",
                option1="x = 2",
                option2="x = -2",
                option3="x = 2, x = -2",
                option4="x = 2 (double root)",
                correct_option=4
            ),
            Question(
                quiz_id=quiz7.id,
                question_statement="If a + b = 5 and ab = 6, what is a² + b²?",
                option1="13",
                option2="25",
                option3="11",
                option4="17",
                correct_option=1
            ),
            Question(
                quiz_id=quiz7.id,
                question_statement="What is the sum of the first 10 terms of an arithmetic sequence with a₁ = 2 and d = 3?",
                option1="155",
                option2="165",
                option3="175",
                option4="185",
                correct_option=2
            )
        ]

        # Questions for Quiz 8 (Advanced Geometry)
        questions8 = [
            Question(
                quiz_id=quiz8.id,
                question_statement="What is the volume of a sphere with radius 3 units?",
                option1="36π cubic units",
                option2="108π cubic units",
                option3="9π cubic units",
                option4="72π cubic units",
                correct_option=1
            ),
            Question(
                quiz_id=quiz8.id,
                question_statement="In a right triangle, if one angle is 30°, what is the ratio of the shortest side to the hypotenuse?",
                option1="1:1",
                option2="1:2",
                option3="1:3",
                option4="2:3",
                correct_option=2
            ),
            Question(
                quiz_id=quiz8.id,
                question_statement="What is the area of a regular hexagon with side length 4 units?",
                option1="24√3 square units",
                option2="48 square units",
                option3="16√3 square units",
                option4="32 square units",
                correct_option=1
            )
        ]

        # Questions for Quiz 9 (Advanced Chemistry)
        questions9 = [
            Question(
                quiz_id=quiz9.id,
                question_statement="What is the molecular mass of glucose (C₆H₁₂O₆)?",
                option1="180 g/mol",
                option2="186 g/mol",
                option3="172 g/mol",
                option4="192 g/mol",
                correct_option=1
            ),
            Question(
                quiz_id=quiz9.id,
                question_statement="Which quantum number determines the shape of an orbital?",
                option1="Principal quantum number",
                option2="Angular momentum quantum number",
                option3="Magnetic quantum number",
                option4="Spin quantum number",
                correct_option=2
            ),
            Question(
                quiz_id=quiz9.id,
                question_statement="What is the hybridization of carbon in ethene (C₂H₄)?",
                option1="sp",
                option2="sp²",
                option3="sp³",
                option4="sp³d",
                correct_option=2
            )
        ]

        # Questions for Quiz 10 (Expired - Basic Algebra Review)
        questions10 = [
            Question(
                quiz_id=quiz10.id,
                question_statement="Simplify: (x² + 2x + 1) - (x² - 2x + 1)",
                option1="4x",
                option2="2x",
                option3="0",
                option4="4x + 2",
                correct_option=1
            ),
            Question(
                quiz_id=quiz10.id,
                question_statement="Factor completely: x² - 4",
                option1="(x + 2)(x - 2)",
                option2="(x + 2)²",
                option3="(x - 2)²",
                option4="x(x - 4)",
                correct_option=1
            )
        ]

        # Questions for Quiz 11 (Expired - Basic Physics Review)
        questions11 = [
            Question(
                quiz_id=quiz11.id,
                question_statement="What is the acceleration due to gravity on Earth (approximate)?",
                option1="9.8 m/s²",
                option2="8.9 m/s²",
                option3="10.0 m/s²",
                option4="7.8 m/s²",
                correct_option=1
            ),
            Question(
                quiz_id=quiz11.id,
                question_statement="Which of these is NOT a vector quantity?",
                option1="Velocity",
                option2="Force",
                option3="Temperature",
                option4="Acceleration",
                correct_option=3
            )
        ]

        # Questions for Quiz 12 (Available now - English - Nouns)
        questions12 = [
            Question(
                quiz_id=quiz12.id,
                question_statement="Which of the following is a proper noun?",
                option1="city",
                option2="London",
                option3="car",
                option4="tree",
                correct_option=2
            ),
            Question(
                quiz_id=quiz12.id,
                question_statement="Identify the noun in the sentence: 'The cat sat on the mat.'",
                option1="cat",
                option2="sat",
                option3="on",
                option4="the",
                correct_option=1
            )
        ]

        # Questions for Quiz 13 (Available now - English - Verbs)
        questions13 = [
            Question(
                quiz_id=quiz13.id,
                question_statement="Which of the following is a verb?",
                option1="run",
                option2="quickly",
                option3="beautiful",
                option4="happiness",
                correct_option=1
            ),
            Question(
                quiz_id=quiz13.id,
                question_statement="Identify the verb in the sentence: 'She sings beautifully.'",
                option1="She",
                option2="sings",
                option3="beautifully",
                option4="the",
                correct_option=2
            )
        ]

        # Questions for Quiz 14 (Available later today - English - Adjectives)
        questions14 = [
            Question(
                quiz_id=quiz14.id,
                question_statement="Which of the following is an adjective?",
                option1="happy",
                option2="run",
                option3="quickly",
                option4="happiness",
                correct_option=1
            ),
            Question(
                quiz_id=quiz14.id,
                question_statement="Identify the adjective in the sentence: 'The quick brown fox jumps over the lazy dog.'",
                option1="quick",
                option2="fox",
                option3="jumps",
                option4="over",
                correct_option=1
            )
        ]

        # Questions for Quiz 15 (Available tomorrow - English - Nouns)
        questions15 = [
            Question(
                quiz_id=quiz15.id,
                question_statement="Which of the following is a common noun?",
                option1="dog",
                option2="Fido",
                option3="London",
                option4="Monday",
                correct_option=1
            ),
            Question(
                quiz_id=quiz15.id,
                question_statement="Identify the noun in the sentence: 'The children are playing in the park.'",
                option1="children",
                option2="are",
                option3="playing",
                option4="in",
                correct_option=1
            )
        ]

        # Questions for Quiz 16 (Available yesterday - English - Adjectives)
        questions16 = [
            Question(
                quiz_id=quiz16.id,
                question_statement="Which of the following is an adjective?",
                option1="blue",
                option2="run",
                option3="quickly",
                option4="happiness",
                correct_option=1
            ),
            Question(
                quiz_id=quiz16.id,
                question_statement="Identify the adjective in the sentence: 'The tall man walked slowly.'",
                option1="tall",
                option2="man",
                option3="walked",
                option4="slowly",
                correct_option=1
            )
        ]
        
        for q in questions1 + questions2 + questions3 + questions4 + questions5 + questions6 + questions7 + questions8 + questions9 + questions10 + questions11 + questions12 + questions13 + questions14 + questions15 + questions16:
            db.session.add(q)
        
        db.session.commit()
        
        # Add scores for expired quizzes
        # Get the test user
        test_user = User.query.filter_by(username="testuser").first()
        
        # Score for Quiz 4 (Chemistry quiz from yesterday)
        score4 = Score(
            user_id=test_user.id,
            quiz_id=quiz4.id,
            total_score=1,  # Got 1 out of 2 questions correct
            max_score=2,
        )
        
        # Score for Quiz 10 (Algebra quiz from 2 days ago)
        score10 = Score(
            user_id=test_user.id,
            quiz_id=quiz10.id,
            total_score=2,  # Got both questions correct
            max_score=2,
        )
        
        # Score for Quiz 11 (Physics quiz from 3 days ago)
        score11 = Score(
            user_id=test_user.id,
            quiz_id=quiz11.id,
            total_score=1,  # Got 1 out of 2 questions correct
            max_score=2,
        )

        # Score for Quiz 12 (English - Nouns)
        score12 = Score(
            user_id=test_user.id,
            quiz_id=quiz12.id,
            total_score=2,  # Got both questions correct
            max_score=2,   
        )

        test_user2 = User.query.filter_by(username="testuser2").first()

        # Score for Quiz 13 (English - Verbs)
        score13 = Score(
            user_id=test_user.id,
            quiz_id=quiz13.id,
            total_score=1,  # Got 1 out of 2 questions correct
            max_score=2,
        )

        # Score for Quiz 16 (English - Adjectives)
        score16 = Score(
            user_id=test_user.id,
            quiz_id=quiz16.id,
            total_score=2,  # Got both questions correct
            max_score=2,
        )

        # Score for Quiz 4 (Chemistry quiz from yesterday) for test_user2
        score4_user2 = Score(
            user_id=test_user2.id,
            quiz_id=quiz4.id,
            total_score=1,  # Got 1 out of 2 questions correct
            max_score=2,
        )

        # Score for Quiz 10 (Algebra quiz from 2 days ago) for test_user2
        score10_user2 = Score(
            user_id=test_user2.id,
            quiz_id=quiz10.id,
            total_score=2,  # Got both questions correct
            max_score=2,
        )

        # Score for Quiz 11 (Physics quiz from 3 days ago) for test_user2
        score11_user2 = Score(
            user_id=test_user2.id,
            quiz_id=quiz11.id,
            total_score=1,  # Got 1 out of 2 questions correct
            max_score=2,
        )

        # Score for Quiz 12 (English - Nouns) for test_user2
        score12_user2 = Score(
            user_id=test_user2.id,
            quiz_id=quiz12.id,
            total_score=2,  # Got both questions correct
            max_score=2,
        )

        # Score for Quiz 13 (English - Verbs) for test_user2
        score13_user2 = Score(
            user_id=test_user2.id,
            quiz_id=quiz13.id,
            total_score=1,  # Got 1 out of 2 questions correct
            max_score=2,
        )

        # Score for Quiz 16 (English - Adjectives) for test_user2
        score16_user2 = Score(
            user_id=test_user2.id,
            quiz_id=quiz16.id,
            total_score=2,  # Got both questions correct
            max_score=2,
        )
        
        db.session.add(score4)
        db.session.add(score10)
        db.session.add(score11)
        db.session.add(score12)
        db.session.add(score13)
        db.session.add(score16)
        db.session.add(score4_user2)
        db.session.add(score10_user2)
        db.session.add(score11_user2)
        db.session.add(score12_user2)
        db.session.add(score13_user2)
        db.session.add(score16_user2)
        db.session.commit()
        print("Database setup complete!")
        print(f"Current time: {now}")
        print(f"Quiz 1 (Available now): {today} from {quiz1.start_time} to {quiz1.end_time}")
        print(f"Quiz 2 (Available later today): {today} from {quiz2.start_time} to {quiz2.end_time}")
        print(f"Quiz 3 (Available tomorrow): {tomorrow} from {quiz3.start_time} to {quiz3.end_time}")
        print(f"Quiz 4 (Expired): {yesterday} from {quiz4.start_time} to {quiz4.end_time}")
        print(f"Quiz 5 (Available now): {today} from {quiz5.start_time} to {quiz5.end_time}")
        print(f"Quiz 6 (Available now): {today} from {quiz6.start_time} to {quiz6.end_time}")
        print(f"Quiz 7 (Available later today): {today} from {quiz7.start_time} to {quiz7.end_time}")
        print(f"Quiz 8 (Available tomorrow): {tomorrow} from {quiz8.start_time} to {quiz8.end_time}")
        print(f"Quiz 9 (Available tomorrow): {tomorrow} from {quiz9.start_time} to {quiz9.end_time}")
        print(f"Quiz 10 (Expired): {two_days_ago} from {quiz10.start_time} to {quiz10.end_time}")
        print(f"Quiz 11 (Expired): {three_days_ago} from {quiz11.start_time} to {quiz11.end_time}")
        print(f"Quiz 12 (Available now): {today} from {quiz12.start_time} to {quiz12.end_time}")
        print(f"Quiz 13 (Available now): {today} from {quiz13.start_time} to {quiz13.end_time}")
        print(f"Quiz 14 (Available later today): {today} from {quiz14.start_time} to {quiz14.end_time}")
        print(f"Quiz 15 (Available tomorrow): {tomorrow} from {quiz15.start_time} to {quiz15.end_time}")
        print(f"Quiz 16 (Available yesterday): {yesterday} from {quiz16.start_time} to {quiz16.end_time}")
        print("\nLogin credentials:")
        print("Admin - Username: admin, Password: password")
        print("User - Username: testuser, Password: password")
        print("User2 - Username: testuser2, Password: password")

if __name__ == "__main__":
    setup_test_db() 