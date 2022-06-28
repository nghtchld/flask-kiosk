from kiosk import app

import os
import logging as log
from flask import render_template, redirect, make_response, flash, url_for, request, session
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
# import duckdb as db
from kiosk.config import Config
from kiosk.utils import log_debug, Item
from kiosk.testform import LoginForm
from kiosk.models import User, Food

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
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        log.debug(f"Checking username...")
        user = User.query.filter_by(username=form.username.data).first()
        log.debug(f"Checking password...")
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            log.info('Invalid username or password')
            return redirect(url_for('login'))
        log.info('Logging in user: {user}')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html.jinja', title='Sign In', form=form)

# favicon.ico (Tab Icon) because the favicon would not be accessible in the root directory (Because of the way Flask works)
@app.route("/favicon.ico")
def favicon():
    try:
        with open("/kisok/res/favicon.ico", "rb") as f:
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
def menu():
    """Pulls menu items from Food model table and list them
    """
    menu_list = []
    menu = Food.query.all()
    log.debug(f"Printing out Food model table")
    for row in menu:
        log.debug(f"This is the row from line 78:")
        log.debug(f"{row.id}, {row.item}, {row.price}, {row.description}")
        menu_list.append([row.id, row.item, round(row.price,2), row.description, row.img])
    log.debug(menu)

    return render_template("menu.html.jinja", title="Menu", menu=menu_list)

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