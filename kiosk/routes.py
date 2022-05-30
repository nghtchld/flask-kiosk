from kiosk import app
from flask import render_template, redirect, make_response, flash, url_for, request, session
import logging as log
from hashlib import blake2b
import os

import duckdb as db

from kiosk.config import Config
from kiosk.utils import log_debug, Item
from kiosk.testform import LoginForm

log_debug()
config = Config()

#-# BEGIN ROUTE DECLARATIONS #-#
@app.route("/")
def index():
    # user = request.args['messages']
    try:
        user = session['user']
    except KeyError:
        user = "Stranger"
    return render_template("index.html.jinja", title="Home", user=user)

@app.route("/login", methods=["GET", "POST"])
def login(DB=config.DB):
    form = LoginForm()
    if form.validate_on_submit():
        log.debug(f"Hashing password...")
        hashed_pw = blake2b(form.password.data.encode('utf-8')).hexdigest()
        log.debug(f"Hashed password: {hashed_pw[32]}")
        con = db.connect(DB)
        log.debug(f"Saving user to main.users TABLE: {form.username.data}")
        log.debug(f"""INSERT INTO main.users (name, pass, save) VALUES
                    {form.username.data}, {hashed_pw[32]}, {form.remember_me.data}
                    ;""")
        con.execute(f"INSERT INTO main.users (uid, name, pass, save) VALUES (uuid(), '{form.username.data}', '{hashed_pw}', {form.remember_me.data});")
        log.debug(f"User data saved.")
        con.close()
        
        user = form.username.data
        session['user'] = user
        
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index', user=user))
    return render_template('login.html.jinja', title = 'Sign In', form=form)
    # if request.method == "POST":
    #     log.info(f"Login attempt with email {request.form.get('email')} and password {request.form.get('password')}")
    # return make_response(render_template("login.html.jinja"), 200)

# favicon.ico (Tab Icon) because the favicon would not be accessible in the root directory (Because of the way Flask works)
@app.route("/favicon.ico")
def favicon():
    try:
        with open("res/favicon.ico", "rb") as f:
            r = make_response(f.read(), 200)
            r.headers["Content-Type"] = "image/x-icon"
            return r
    except FileNotFoundError as e:
        log.error(str(e) + " in " + os.getcwd())
        return make_response("", 500)
    except Exception as e:
        log.error(e)
        return make_response("", 500)

@app.route("/cart")
def cart():
    # Temporary
    cart = [
        Item("1", "Chicken", 10, "White meat", "/res/default.png", {}),
        Item("2", "Beef", 20, "Red meat", "/res/default.png", {}),
        Item("3", "Pork", 30, "Other white meat", "/res/default.png", {}),
        Item("4", "Fish", 40, "Sea meat", "/res/default.png", {})
    ]
    return render_template("cart.html.jinja", title="Cart", order=cart)

@app.route("/menu")
def menu(DB=config.DB):
    """Pulls menu items from main.foods table and list them
    """
    menu = []
    con = db.connect(DB)
    con.execute("SELECT * FROM main.foods")
    menu_table = con.fetchall()
    log.debug(f"Printing out main.foods TABLE: {menu_table}")
    for row in menu_table:
        log.debug(f"This is the row from line 62 {row}")
        menu.append(Item(*row))
    log.debug(menu)
    con.close()

    return render_template("menu.html.jinja", title="Menu", menu=menu)

@app.route("/cart/<int:id>")
def cartItem(id):
    return make_response(render_template("403.html.jinja"), 403)

@app.route("/403")
def forboden():
    return make_response(render_template("403.html.jinja"), 403)

#-# SPECIAL ROUTES #-#

@app.errorhandler(404)
def not_found(e):
    return make_response(render_template("404.html.jinja"), 404)

@app.errorhandler(403)
def forbidden(e):
    return make_response(render_template("403.html.jinja"), 403)

@app.after_request
def after_request(r):
    # Set headers to prevent caching
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r