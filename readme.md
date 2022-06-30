# Restaurant Kiosk: a Flask Web App   
This repo contains a [Flask](https://palletsprojects.com/p/flask/) web application with an [sqlite](https://sqlite.org/) Dev database using flask-sqlalchemy
### Features 
- Working flask/jinja website with templates (HTML, JS, CSS)
- Working flask-sqlalchemy defined sqlite (dev) database setup with initial data insertion
- Working Flask-WTF forms 
- TODO UPDATE to use flask-login
- Working session username usage (only for index atm)
- TODO UPDATE to use flask-login
- Working menu selected from db
- TODO Ordering system
- TODO Menu item customisation on order
- TODO Admin Panel (Ability to create discounts, Foods and customisations )
# Installation
## used venv for virtual environment setup 
py -m venv --prompt "flask-kiosk" --upgrade-deps c:\Users\USERNAME\.venv\flask-kiosk

## Activate virtual env and generate a better requirements.txt with pip-tools
`C:\Users\USERNAME\.venv\flask-kiosk\Scripts\activate.bat`

`pip install -r requirements.txt`

`pip freeze > requirements.in`

Edit the `requirements.in` file above to only list the packages from the original requirements.txt

`py -m piptools compile --output-file=requirements.txt requirements.in`

## .env in root folder or ENV variables needed
a root `.env` file is needed by `/kiosk/config.py` for at least a SALT (> 8 characters long) and a DATABASE name defined. Its template is:

    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    PORT = os.getenv('PORT', '8080')
    SALT = os.getenv('SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

