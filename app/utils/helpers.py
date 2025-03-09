import re
from werkzeug.security import generate_password_hash
from app.models.database import Admin, db

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def create_admin():
    if not Admin.query.filter(
        (Admin.username == 'admin') | 
        (Admin.email == 'admin@quizmaster.com')
    ).first():
        admin = Admin(
            username='admin',
            email='admin@quizmaster.com',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit() 