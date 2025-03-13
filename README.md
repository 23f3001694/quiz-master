# Quiz Master

A robust web application for creating, managing, and taking quizzes built with Flask and SQLAlchemy.

## Features

- User authentication and authorization
- Create and manage quizzes
- Take quizzes and view results
- RESTful API support
- Admin dashboard for user management
- Responsive design using Bootstrap

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Jinja2 Templates
- **Authentication**: Flask-Login
- **API Documentation**: Postman Collection included

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/23f3001694/quiz-master.git
cd quiz-master
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python setup_test_db.py
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
quiz-master/
├── app/                    # Application package
│   ├── models/            # Database models
│   ├── routes/            # Route handlers
│   ├── templates/         # Jinja2 templates
│   ├── utils/             # Utility functions
│   └── __init__.py        # App initialization
├── instance/              # Instance-specific files
├── docs/                  # Documentation
├── venv/                  # Virtual environment
├── app.py                 # Application entry point
├── requirements.txt       # Project dependencies
├── setup_test_db.py      # Database setup script
└── Quiz Master API.postman_collection.json  # API documentation
```

## API Documentation

The project includes a Postman collection (`Quiz Master API.postman_collection.json`) that documents all available API endpoints. Import this collection into Postman to explore and test the API.

## Development

To set up the development environment:

1. Install development dependencies
2. Follow the installation steps above
3. Make your changes
4. Run tests before submitting pull requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## References and Sources

### Documentation Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)

### Additional Resources

- [Flask Decorators](https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/)
- [Flask Blueprints Tutorial](https://realpython.com/flask-blueprint/)
- [Flask Templates Guide](https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application)
- [Flask Sessions Guide](https://testdriven.io/blog/flask-sessions/)

## Acknowledgments

Special thanks to:
- The Flask community for excellent documentation
- Contributors and maintainers of all used packages
- Language models (LLMs) for development assistance and insights

