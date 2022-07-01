from kiosk import app

import os
import logging as log
from flask import render_template, redirect, make_response, flash, url_for, session, send_from_directory
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
# import duckdb as db
from kiosk.config import Config
from kiosk.utils import log_debug, Item
from kiosk.forms import LoginForm
from kiosk.models import User, Food
from kiosk.db_init import init_food_table

log_debug()
config = Config()

#-# BEGIN ROUTE DECLARATIONS #-#
@app.route("/")
@app.route('/index')
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
        log.info(f"current_user is: {current_user}")
        return redirect(url_for('index'))
    return render_template('login.html.jinja', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# favicon.ico (Tab Icon) because the favicon would not be accessible in the root directory (Because of the way Flask works)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'res'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



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
    # check Food table for contents
    init_food_table()
    menu_list = []
    menu = Food.query.all()
    log.debug(f"Listing items in Food model table as menu...")
    for row in menu:
        menu_list.append([row.id, row.item, round(row.price,2), row.description, row.img])
    log.debug(f"Menu list is: {menu}")

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