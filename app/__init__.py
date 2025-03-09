from flask import Flask
from app.models.database import db
from app.routes.auth import auth
from app.routes.admin import admin
from app.routes.user import user
from datetime import datetime

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'hail-hydra'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
    app.config['DEBUG'] = True

    # Add now() function to Jinja environment
    app.jinja_env.globals.update(now=datetime.now)

    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)

    with app.app_context():
        db.create_all()

    return app 