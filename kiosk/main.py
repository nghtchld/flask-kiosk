# @name Restaurant Kiosk
# Derived with grudging perminssion from @author: Ash Skabo
# @author: Stuart Skabo
# @copyright: Creative Commons BY v4.0

##-# IMPORTS #-##
import os
import sys
import logging as log
import random as rd
import string
import re
import hashlib as hl

import duckdb as db

from kiosk.utils import Item, log_debug
from kiosk.config import Config

##-# DECLARATIONS & SET UP #-##
log_debug()
config = Config()

# Change path to own directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

## Load environment variables from .env file
log.info("Loading config...")
log.debug(f'config.DB = {config.DB}')

# If salt is not set or too short, exit.
if config.SALT in (None, ""):
    log.critical(".env does not contain critical 'SALT' value. Cannot continue.")
    sys.exit(1)
elif len(config.SALT) < 8:
    log.critical(".env contains a 'SALT' value that is too short. Cannot continue.")
    sys.exit(1)

## Connect to database
log.info("Connecting database...")
try:
    con = db.connect(config.DB)
except RuntimeError:
    # RuntimeError in this case signifies that the file is inaccessible due to already being used
    log.critical(f"Database file '{config.DB}' already in use. Cannot continue. Is another instance already running?")
    sys.exit(1)

## Check if database is populated and create tables if not
con.execute("SELECT * FROM information_schema.tables WHERE table_name IN ('foods','orders','users','sessions') AND table_schema = 'main'")
tables = con.fetchall()
if len(tables) != 4:
    log.warning("Database is not populated. Populating...")
    con.execute("""CREATE TABLE IF NOT EXISTS main.users (
            uid VARCHAR(32) NOT NULL,
            name VARCHAR(32) NOT NULL,
            pass CHAR(256) NOT NULL,
            save BOOL NOT NULL,
            "data" TEXT DEFAULT '{"priority": 0, "perms": ["default"], "dealsUsed": []}' NOT NULL,
            CONSTRAINT users_PK PRIMARY KEY (uid)
            );
            """)
    # Create sessions table
    con.execute("""CREATE TABLE IF NOT EXISTS main.sessions (
            sid VARCHAR(256) NOT NULL,
            uid INTEGER NOT NULL,
            expires TIMESTAMP NOT NULL,
            CONSTRAINT sessions_PK PRIMARY KEY (sid)
            );
            """)
    # Create foods table (will store all food items and their options in a JSON format)
    con.execute("""CREATE TABLE IF NOT EXISTS main.foods (
            fid VARCHAR(16) NOT NULL,
            name VARCHAR(32) NOT NULL,
            price INTEGER NOT NULL,
            description TEXT NOT NULL,
            img VARCHAR(256) NOT NULL,
            options TEXT DEFAULT '{"size": {"type": "radio", "text": "Size", "options": ["Small", "Medium", "Large"]}}',
            CONSTRAINT foods_PK PRIMARY KEY (fid)
            );
            """)
    # Create orders table (will store current cart and previous orders)
    con.execute("""CREATE TABLE IF NOT EXISTS main.orders (
            oid CHAR(128) NOT NULL,
            uid INTEGER NOT NULL,
            active BOOL NOT NULL,
            data TEXT NOT NULL,
            CONSTRAINT orders_PK PRIMARY KEY (oid)
            );
            """)

# Make sure there is data in the main.foods TABLE
con.execute("SELECT name FROM main.foods")
food_count = con.fetchall()
log.info(f'Menu length is: {str(len(food_count))}')
if len(food_count) < 2:
    log.info('Inserting menu items from menu.csv to main.foods table...')
    try:
        # Fill main.foods table from menu.csv
        con.execute("""COPY main.foods FROM 'menu.csv' (QUOTE '"', HEADER);
                """)
    except NameError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = log.traceback.format_exception(exc_type, exc_value, exc_traceback)
        log.critical("Error loading data from menu.txt to TABLE main.foods:")
        log.critical( ''.join('!! ' + line for line in lines))

con.close()