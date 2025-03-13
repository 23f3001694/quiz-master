from flask import Blueprint, jsonify, request
from app.models.database import db, Subject, Chapter, Quiz, Question, Score, User
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/subjects', methods=['GET'])
def get_subjects():
    """Get all subjects.
    
    Returns:
        JSON: A list of all subjects with their id, name, and description.
        Format: [{'id': int, 'name': str, 'description': str}, ...]
    """
    subjects = Subject.query.all()
    result = []
    for subject in subjects:
        result.append({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        })
    return jsonify(result)

@api.route('/subjects/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    """Get a specific subject by ID.
    
    Args:
        subject_id (int): The ID of the subject to retrieve.
    
    Returns:
        JSON: Subject details including id, name, and description.
        Format: {'id': int, 'name': str, 'description': str}
        
    Raises:
        404: If subject is not found.
    """
    subject = Subject.query.get_or_404(subject_id)
    return jsonify({
        'id': subject.id,
        'name': subject.name,
        'description': subject.description
    })

@api.route('/subjects', methods=['POST'])
def create_subject():
    """Create a new subject.
    
    Request Body:
        {
            'name': str (required),
            'description': str (optional)
        }
    
    Returns:
        JSON: The created subject's details.
        Format: {'id': int, 'name': str, 'description': str}
        
    Raises:
        400: If name is not provided or other validation errors occur.
    """
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    subject = Subject(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(subject)
    
    try:
        db.session.commit()
        return jsonify({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/subjects/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    """Update an existing subject.
    
    Args:
        subject_id (int): The ID of the subject to update.
    
    Request Body:
        {
            'name': str (optional),
            'description': str (optional)
        }
    
    Returns:
        JSON: The updated subject's details.
        Format: {'id': int, 'name': str, 'description': str}
        
    Raises:
        404: If subject is not found.
        400: If validation errors occur.
    """
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    if 'name' in data:
        subject.name = data['name']
    if 'description' in data:
        subject.description = data['description']
    
    try:
        db.session.commit()
        return jsonify({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    """Delete a subject.
    
    Args:
        subject_id (int): The ID of the subject to delete.
    
    Returns:
        JSON: Success message.
        Format: {'message': str}
        
    Raises:
        404: If subject is not found.
        400: If deletion fails.
    """
    subject = Subject.query.get_or_404(subject_id)
    
    try:
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'message': 'Subject deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/chapters', methods=['GET'])
def get_chapters():
    """Get all chapters or chapters for a specific subject.
    
    Query Parameters:
        subject_id (int, optional): Filter chapters by subject ID.
    
    Returns:
        JSON: List of chapters with their details.
        Format: [{'id': int, 'subject_id': int, 'name': str, 'description': str}, ...]
    """
    subject_id = request.args.get('subject_id', type=int)
    
    if subject_id:
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    else:
        chapters = Chapter.query.all()
    
    result = []
    for chapter in chapters:
        result.append({
            'id': chapter.id,
            'subject_id': chapter.subject_id,
            'name': chapter.name,
            'description': chapter.description
        })
    return jsonify(result)

@api.route('/chapters/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    """Get a specific chapter by ID.
    
    Args:
        chapter_id (int): The ID of the chapter to retrieve.
    
    Returns:
        JSON: Chapter details.
        Format: {'id': int, 'subject_id': int, 'name': str, 'description': str}
        
    Raises:
        404: If chapter is not found.
    """
    chapter = Chapter.query.get_or_404(chapter_id)
    return jsonify({
        'id': chapter.id,
        'subject_id': chapter.subject_id,
        'name': chapter.name,
        'description': chapter.description
    })

@api.route('/chapters', methods=['POST'])
def create_chapter():
    """Create a new chapter.
    
    Request Body:
        {
            'name': str (required),
            'subject_id': int (required),
            'description': str (optional)
        }
    
    Returns:
        JSON: The created chapter's details.
        Format: {'id': int, 'subject_id': int, 'name': str, 'description': str}
        
    Raises:
        400: If required fields are missing or validation fails.
        404: If subject_id does not exist.
    """
    data = request.get_json()
    
    if not data or 'name' not in data or 'subject_id' not in data:
        return jsonify({'error': 'Name and subject_id are required'}), 400
    
    subject = Subject.query.get(data['subject_id'])
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    
    chapter = Chapter(
        name=data['name'],
        subject_id=data['subject_id'],
        description=data.get('description', '')
    )
    
    db.session.add(chapter)
    
    try:
        db.session.commit()
        return jsonify({
            'id': chapter.id,
            'subject_id': chapter.subject_id,
            'name': chapter.name,
            'description': chapter.description
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/chapters/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    """Update an existing chapter.
    
    Args:
        chapter_id (int): The ID of the chapter to update.
    
    Request Body:
        {
            'name': str (optional),
            'description': str (optional),
            'subject_id': int (optional)
        }
    
    Returns:
        JSON: The updated chapter's details.
        Format: {'id': int, 'subject_id': int, 'name': str, 'description': str}
        
    Raises:
        404: If chapter is not found or if new subject_id does not exist.
        400: If validation errors occur.
    """
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    
    if 'name' in data:
        chapter.name = data['name']
    if 'description' in data:
        chapter.description = data['description']
    if 'subject_id' in data:
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        chapter.subject_id = data['subject_id']
    
    try:
        db.session.commit()
        return jsonify({
            'id': chapter.id,
            'subject_id': chapter.subject_id,
            'name': chapter.name,
            'description': chapter.description
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/chapters/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    """Delete a chapter.
    
    Args:
        chapter_id (int): The ID of the chapter to delete.
    
    Returns:
        JSON: Success message.
        Format: {'message': str}
        
    Raises:
        404: If chapter is not found.
        400: If deletion fails.
    """
    chapter = Chapter.query.get_or_404(chapter_id)
    
    try:
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({'message': 'Chapter deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/quizzes', methods=['GET'])
def get_quizzes():
    """Get all quizzes or quizzes for a specific chapter.
    
    Query Parameters:
        chapter_id (int, optional): Filter quizzes by chapter ID.
    
    Returns:
        JSON: List of quizzes with their details.
        Format: [{
            'id': int,
            'chapter_id': int,
            'date_of_quiz': str (ISO format),
            'start_time': str (ISO format),
            'end_time': str (ISO format),
            'time_duration': str
        }, ...]
    """
    chapter_id = request.args.get('chapter_id', type=int)
    
    if chapter_id:
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    else:
        quizzes = Quiz.query.all()
    
    result = []
    for quiz in quizzes:
        result.append({
            'id': quiz.id,
            'chapter_id': quiz.chapter_id,
            'date_of_quiz': quiz.date_of_quiz.isoformat() if quiz.date_of_quiz else None,
            'start_time': quiz.start_time.isoformat() if quiz.start_time else None,
            'end_time': quiz.end_time.isoformat() if quiz.end_time else None,
            'time_duration': quiz.time_duration
        })
    return jsonify(result)

@api.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a specific quiz by ID, including its questions.
    
    Args:
        quiz_id (int): The ID of the quiz to retrieve.
    
    Returns:
        JSON: Quiz details including all questions.
        Format: {
            'id': int,
            'chapter_id': int,
            'date_of_quiz': str (ISO format),
            'start_time': str (ISO format),
            'end_time': str (ISO format),
            'time_duration': str,
            'questions': [{
                'id': int,
                'question_statement': str,
                'option1': str,
                'option2': str,
                'option3': str,
                'option4': str,
                'correct_option': int
            }, ...]
        }
        
    Raises:
        404: If quiz is not found.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    
    questions = []
    for question in quiz.questions:
        questions.append({
            'id': question.id,
            'question_statement': question.question_statement,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
            'correct_option': question.correct_option
        })
    
    return jsonify({
        'id': quiz.id,
        'chapter_id': quiz.chapter_id,
        'date_of_quiz': quiz.date_of_quiz.isoformat() if quiz.date_of_quiz else None,
        'start_time': quiz.start_time.isoformat() if quiz.start_time else None,
        'end_time': quiz.end_time.isoformat() if quiz.end_time else None,
        'time_duration': quiz.time_duration,
        'questions': questions
    })

@api.route('/quizzes', methods=['POST'])
def create_quiz():
    """Create a new quiz with optional questions.
    
    Request Body:
        {
            'chapter_id': int (required),
            'date_of_quiz': str (required, ISO format),
            'start_time': str (required, format: HH:MM:SS),
            'end_time': str (required, format: HH:MM:SS),
            'time_duration': str (optional),
            'questions': [{ # optional
                'question_statement': str (required),
                'option1': str (required),
                'option2': str (required),
                'option3': str (required),
                'option4': str (required),
                'correct_option': int (required)
            }, ...]
        }
    
    Returns:
        JSON: The created quiz's details.
        Format: {
            'id': int,
            'chapter_id': int,
            'date_of_quiz': str (ISO format),
            'start_time': str (ISO format),
            'end_time': str (ISO format),
            'time_duration': str
        }
        
    Raises:
        400: If required fields are missing or validation fails.
        404: If chapter_id does not exist.
    """
    data = request.get_json()
    
    if not data or 'chapter_id' not in data or 'date_of_quiz' not in data or 'start_time' not in data or 'end_time' not in data:
        return jsonify({'error': 'chapter_id, date_of_quiz, start_time, and end_time are required'}), 400
    
    chapter = Chapter.query.get(data['chapter_id'])
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    
    try:
        date_of_quiz = datetime.fromisoformat(data['date_of_quiz'])
        
        start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
        
        time_duration = data.get('time_duration', '')
        if time_duration:
            try:
                duration_mins = int(time_duration)
                if duration_mins <= 0:
                    return jsonify({'error': 'time_duration must be a positive number'}), 400
                time_duration = f"{duration_mins} mins"
            except ValueError:
                return jsonify({'error': 'time_duration must be a valid number'}), 400
        
        quiz = Quiz(
            chapter_id=data['chapter_id'],
            date_of_quiz=date_of_quiz,
            start_time=start_time,
            end_time=end_time,
            time_duration=time_duration
        )
        
        db.session.add(quiz)
        db.session.commit()
        
        if 'questions' in data and isinstance(data['questions'], list):
            for q_data in data['questions']:
                if all(key in q_data for key in ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']):
                    question = Question(
                        quiz_id=quiz.id,
                        question_statement=q_data['question_statement'],
                        option1=q_data['option1'],
                        option2=q_data['option2'],
                        option3=q_data['option3'],
                        option4=q_data['option4'],
                        correct_option=q_data['correct_option']
                    )
                    db.session.add(question)
            
            db.session.commit()
        
        return jsonify({
            'id': quiz.id,
            'chapter_id': quiz.chapter_id,
            'date_of_quiz': quiz.date_of_quiz.isoformat(),
            'start_time': quiz.start_time.isoformat(),
            'end_time': quiz.end_time.isoformat(),
            'time_duration': quiz.time_duration
        }), 201
    
    except ValueError as e:
        return jsonify({'error': f'Invalid date or time format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    """Update an existing quiz.
    
    Args:
        quiz_id (int): The ID of the quiz to update.
    
    Request Body:
        {
            'chapter_id': int (optional),
            'date_of_quiz': str (optional, ISO format),
            'start_time': str (optional, format: HH:MM:SS),
            'end_time': str (optional, format: HH:MM:SS),
            'time_duration': str (optional)
        }
    
    Returns:
        JSON: The updated quiz's details.
        Format: {
            'id': int,
            'chapter_id': int,
            'date_of_quiz': str (ISO format),
            'start_time': str (ISO format),
            'end_time': str (ISO format),
            'time_duration': str
        }
        
    Raises:
        404: If quiz is not found or if new chapter_id does not exist.
        400: If validation errors occur.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    try:
        if 'chapter_id' in data:
            chapter = Chapter.query.get(data['chapter_id'])
            if not chapter:
                return jsonify({'error': 'Chapter not found'}), 404
            quiz.chapter_id = data['chapter_id']
        
        if 'date_of_quiz' in data:
            quiz.date_of_quiz = datetime.fromisoformat(data['date_of_quiz'])
        
        if 'start_time' in data:
            quiz.start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        
        if 'end_time' in data:
            quiz.end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
        
        if 'time_duration' in data:
            time_duration = data['time_duration']
            try:
                duration_mins = int(time_duration)
                if duration_mins <= 0:
                    return jsonify({'error': 'time_duration must be a positive number'}), 400
                quiz.time_duration = f"{duration_mins} mins"
            except ValueError:
                return jsonify({'error': 'time_duration must be a valid number'}), 400
        
        db.session.commit()
        
        return jsonify({
            'id': quiz.id,
            'chapter_id': quiz.chapter_id,
            'date_of_quiz': quiz.date_of_quiz.isoformat(),
            'start_time': quiz.start_time.isoformat(),
            'end_time': quiz.end_time.isoformat(),
            'time_duration': quiz.time_duration
        })
    
    except ValueError as e:
        return jsonify({'error': f'Invalid date or time format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Delete a quiz.
    
    Args:
        quiz_id (int): The ID of the quiz to delete.
    
    Returns:
        JSON: Success message.
        Format: {'message': str}
        
    Raises:
        404: If quiz is not found.
        400: If deletion fails.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    
    try:
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({'message': 'Quiz deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/scores', methods=['GET'])
def get_scores():
    """Get all scores or filter by user_id and/or quiz_id.
    
    Query Parameters:
        user_id (int, optional): Filter scores by user ID.
        quiz_id (int, optional): Filter scores by quiz ID.
    
    Returns:
        JSON: List of scores with calculated percentages.
        Format: [{
            'id': int,
            'user_id': int,
            'quiz_id': int,
            'total_score': float,
            'max_score': float,
            'percentage': float
        }, ...]
    """
    user_id = request.args.get('user_id', type=int)
    quiz_id = request.args.get('quiz_id', type=int)
    
    query = Score.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    if quiz_id:
        query = query.filter_by(quiz_id=quiz_id)
    
    scores = query.all()
    
    result = []
    for score in scores:
        result.append({
            'id': score.id,
            'user_id': score.user_id,
            'quiz_id': score.quiz_id,
            'total_score': score.total_score,
            'max_score': score.max_score,
            'percentage': (score.total_score / score.max_score * 100) if score.max_score > 0 else 0
        })
    
    return jsonify(result)

@api.route('/scores/<int:score_id>', methods=['GET'])
def get_score(score_id):
    """Get a specific score by ID.
    
    Args:
        score_id (int): The ID of the score to retrieve.
    
    Returns:
        JSON: Score details with calculated percentage.
        Format: {
            'id': int,
            'user_id': int,
            'quiz_id': int,
            'total_score': float,
            'max_score': float,
            'percentage': float
        }
        
    Raises:
        404: If score is not found.
    """
    score = Score.query.get_or_404(score_id)
    
    return jsonify({
        'id': score.id,
        'user_id': score.user_id,
        'quiz_id': score.quiz_id,
        'total_score': score.total_score,
        'max_score': score.max_score,
        'percentage': (score.total_score / score.max_score * 100) if score.max_score > 0 else 0
    })

@api.route('/scores', methods=['POST'])
def create_score():
    """Create a new score entry.
    
    Request Body:
        {
            'user_id': int (required),
            'quiz_id': int (required),
            'total_score': float (required),
            'max_score': float (required)
        }
    
    Returns:
        JSON: The created score details with calculated percentage.
        Format: {
            'id': int,
            'user_id': int,
            'quiz_id': int,
            'total_score': float,
            'max_score': float,
            'percentage': float
        }
        
    Raises:
        400: If required fields are missing or validation fails.
        404: If user_id or quiz_id does not exist.
    """
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'quiz_id' not in data or 'total_score' not in data or 'max_score' not in data:
        return jsonify({'error': 'user_id, quiz_id, total_score, and max_score are required'}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    quiz = Quiz.query.get(data['quiz_id'])
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    score = Score(
        user_id=data['user_id'],
        quiz_id=data['quiz_id'],
        total_score=data['total_score'],
        max_score=data['max_score']
    )
    
    db.session.add(score)
    
    try:
        db.session.commit()
        return jsonify({
            'id': score.id,
            'user_id': score.user_id,
            'quiz_id': score.quiz_id,
            'total_score': score.total_score,
            'max_score': score.max_score,
            'percentage': (score.total_score / score.max_score * 100) if score.max_score > 0 else 0
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/scores/<int:score_id>', methods=['PUT'])
def update_score(score_id):
    """Update an existing score.
    
    Args:
        score_id (int): The ID of the score to update.
    
    Request Body:
        {
            'total_score': float (optional),
            'max_score': float (optional)
        }
    
    Returns:
        JSON: The updated score details with calculated percentage.
        Format: {
            'id': int,
            'user_id': int,
            'quiz_id': int,
            'total_score': float,
            'max_score': float,
            'percentage': float
        }
        
    Raises:
        404: If score is not found.
        400: If validation errors occur.
    """
    score = Score.query.get_or_404(score_id)
    data = request.get_json()
    
    if 'total_score' in data:
        score.total_score = data['total_score']
    
    if 'max_score' in data:
        score.max_score = data['max_score']
    
    try:
        db.session.commit()
        return jsonify({
            'id': score.id,
            'user_id': score.user_id,
            'quiz_id': score.quiz_id,
            'total_score': score.total_score,
            'max_score': score.max_score,
            'percentage': (score.total_score / score.max_score * 100) if score.max_score > 0 else 0
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/scores/<int:score_id>', methods=['DELETE'])
def delete_score(score_id):
    """Delete a score.
    
    Args:
        score_id (int): The ID of the score to delete.
    
    Returns:
        JSON: Success message.
        Format: {'message': str}
        
    Raises:
        404: If score is not found.
        400: If deletion fails.
    """
    score = Score.query.get_or_404(score_id)
    
    try:
        db.session.delete(score)
        db.session.commit()
        return jsonify({'message': 'Score deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 