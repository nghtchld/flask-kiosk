from kiosk import app
from kiosk import db

import os
import logging as log
from datetime import datetime
from flask import render_template, redirect, make_response, flash, url_for, session, send_from_directory, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from kiosk.config import Config
from kiosk.utils import log_debug, Item
from kiosk.forms import LoginForm, RegisterForm
from kiosk.models import User, Food
from kiosk.db_utils import init_food_table, register_user_in_db

log_debug()
config = Config()

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


#-# BEGIN ROUTE DECLARATIONS #-#
@app.route("/")
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user=current_user
    else:
        user = "Stranger"
    log.debug(f"index.html username is: {user}")
    return render_template("index.html.jinja", title="Home", user=user)


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        register_user_in_db(form)
        username=form.username.data
        user = User.query.filter_by(username=username).first()
        log.info('Logging in newly registered db user: {user}. With username {username}')
        login_user(user, remember=form.remember_me.data)
        log.info(f"current_user is: {current_user}")
        flash(f'Congratulations {username}, you are now a registered Mex&Co Compradre!')
        return redirect(url_for('index'))
    return render_template('register.html.jinja', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        log.debug(f"Checking username: '{username}'...")
        user = User.query.filter_by(username=username).first()
        if user is None:
            log.info(f"Unknown user. Redirecting to 'register'.")
            return redirect(url_for('register'))
        elif user.check_password(password) == 0:
            db.session.delete(user)
            return redirect(url_for('register'))
        elif not user.check_password(password):
            flash('Invalid username or password')
            log.info('Invalid password!')
            return redirect(url_for('login'))
        log.info('Logging in db user: {user}. With username {username}')
        login_user(user, remember=form.remember_me.data)
        log.info(f"'{current_user.username}' has logged in.")
        # Check for a next (page) URL argument
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.jinja', title='Sign In', form=form)


@app.route('/logout')
def logout():
    log.info(f"'{current_user.username}' has logged out.")
    logout_user()
    return redirect(url_for('index'))


# Solution from Flask Mega-Tutorial, also added <href...favicon.ico> in template.html.jinja
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'res'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/userpage/<username>')
@login_required
def userpage(username):
    user = User.query.filter_by(username=username).first_or_404()
    # TODO add list of user's orders, favorites etc using a _sub template
    # below are temp placeholder 'orders' by user 'user'
    orders = [
        {'customer': user, 'order': 'Test order #1'},
        {'customer': user, 'order': 'Test order #2'}
    ]
    # sample actual order code might be like:
    # orders = user.orders.all()
    return render_template('userpage.html.jinja', user=user, orders=orders)

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
    for row in menu:
        menu_list.append([row.id, row.item, round(row.price,2), row.description, row.img])
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