# @name Restaurant Kiosk
# Derived with grudging perminssion from:
# @author: Ash Skabo
# @author: Stuart Skabo
# @copyright: Creative Commons BY v4.0

##-# IMPORTS #-##
import os
import sys
import logging as log

from kiosk.utils import log_debug
from kiosk.config import Config

##-# DECLARATIONS & SET UP #-##
log_debug()
log.info("Loading config...")
config = Config()

# Change path to own directory
# os.chdir(os.path.dirname(os.path.realpath(__file__)))

# If salt is not set or too short, exit.
if config.SALT in (None, ""):
    log.critical(".env does not contain critical 'SALT' value. Cannot continue.")
    sys.exit(1)
elif len(config.SALT) < 8:
    log.critical(".env contains a 'SALT' value that is too short. Cannot continue.")
    sys.exit(1)

## Connect to database
# now using SQLAlchemy in __init__.py

# # Make sure there is data in the main.foods TABLE
# menu = Food.query.all()
# log.debug(f"Checking Food model table for contents:")
# log.debug(f"{menu}")
# if len(menu) < 2:
#     filePath = os.path.join('res','menu.csv')
#     log.info('Reading menu file...')
#     reader = csv.DictReader(open(filePath))
#     log.info('Inserting menu items from menu.csv to Food model table...')
#     for row in reader:
#         log.debug(f"Menu row: {row}")#['item']}, {row['price']}, {row['description']}")
#         food = Food(item=row['item'],
#                     price=row['price'],
#                     description=row['description'],
#                     img=row['img'],
#                     options=row['options'])
#         db.session.add(food)
#         db.session.commit()

# con.execute("SELECT name FROM main.foods")
# food_count = con.fetchall()
# log.info(f'Menu length is: {str(len(food_count))}')
# if len(food_count) < 2:
#     log.info('Inserting menu items from menu.csv to main.foods table...')
#     try:
#         # Fill main.foods table from menu.csv
#         con.execute("""COPY main.foods FROM 'menu.csv' (QUOTE '"', HEADER);
#                 """)
#     except NameError:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         lines = log.traceback.format_exception(exc_type, exc_value, exc_traceback)
#         log.critical("Error loading data from menu.txt to TABLE main.foods:")
#         log.critical( ''.join('!! ' + line for line in lines))

# con.close()