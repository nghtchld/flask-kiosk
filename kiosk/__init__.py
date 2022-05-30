import logging as log

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from kiosk.config import Config
from kiosk.utils import log_debug

log_debug()

log.info("Starting server...")
# Define the flask app
app = Flask(__name__, static_folder="res")

# setup flask config
app.config.from_object(Config)

# setting up sqlalchemy and alembic
log.info("Setting up SQLAlchemy...")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
log.info("SQLAlchemy set initialised")

# setup flask routes
log.info("Importing routes...")
from kiosk import routes, models
log.info("Finished importing routes.py")

# replaced with sqlachemy above
# # run main.py database validation and or setup
# log.info("Importing and running main.py, DB setup.")
# import kiosk.main
# log.info("Finished importing main.py")