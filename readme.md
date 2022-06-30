# Restaurant Kiosk: a Flask Web App   
This repo contains a [Flask](https://palletsprojects.com/p/flask/) web application with an [sqlite](https://sqlite.org/) Dev database using flask-sqlalchemy classes. It broadly follows the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). 
# Features 
- Working flask/jinja website with templates (HTML, JS, CSS)
- Working flask-sqlalchemy defined sqlite (dev) database setup with initial data insertion
- Working Flask-WTF forms 
- TODO clean up testform.py, main.py
- Working session username usage (only for index atm)
    TODO UPDATE to use flask-login: 
    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
- Working menu selected from db
- TODO update logging to use wrappers for functions
    see https://towardsdatascience.com/using-wrappers-to-log-in-python
- TODO Ordering system using flask-sqlalchemy Classes
- TODO Menu item customisation on order
- TODO Receipt prodcution with Tax and Tip
- TODO Admin Panel (Ability to create discounts, Foods and customisations )
- TODO add Unit testing: https://realpython.com/python-testing/
    https://code.visualstudio.com/docs/python/testing
- TODO Containerise (Docker): https://code.visualstudio.com/docs/containers/quickstart-python
- TODO Deploy to cloud (AWS, Azure): https://code.visualstudio.com/docs/python/python-on-azure
# Installation
## Use venv for virtual environment setup 
py -m venv --prompt "flask-kiosk" --upgrade-deps c:\Users\USERNAME\.venv\flask-kiosk

## Activate virtual env and generate a better requirements.txt with pip-tools
`C:\Users\USERNAME\.venv\flask-kiosk\Scripts\activate.bat`

`pip install -r requirements.txt`

`pip freeze > requirements.in`

Edit the `requirements.in` file above to only list the packages from the original requirements.txt

`py -m piptools compile --output-file=requirements.txt requirements.in`

## Create a .env file in root folder (or use ENV variables)
a root `.env` file is needed by `/kiosk/config.py` for at least a SALT (> 8 characters long) and a DATABASE name defined. Its template is:
    DATABASE=app.db
    DATABASE_URL=
    SALT=must_have_a_salt_more_than_8_chrs_long
    SECRET_KEY=
    PORT=

## Initialise the database
The app uses the flask-migrate package and so the database schema is under Alembic control. The Alembic migration scripts are in the `/migrations` folder. 

Before running the flask app you need to create and initialise the database.
1. run flask db init (creates a database and sets up migrations)
2. run flask db migrate (creates the upgrade script)
3. run flask db upgrade (upgrades the database to the latest version)

# Licence
This project is licenced under the BSD 3-Clause licence. A full copy of this licene is in the `LICENCE` file. 