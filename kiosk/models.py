import json
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from kiosk import db
from kiosk import login

# flask-migrate alembic in use to manage db changes
# Use cmdline >flask db migrate -m "short message"
# to generate migration script. Inspect script if desired.
# Then cmdline >flask db upgrade
# to upgrade database from model changes in code.

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Session(db.Model):
    id = db.Column(db.String(256), primary_key=True)

    def __repr__(self):
        return f'{self.id}'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String(1024), index=False, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

    def __repr__(self):
        order = self.order
        order_dict = {'Order': order}
        return json.dumps(order_dict)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.Float(10,2), index=False, unique=False)
    description = db.Column(db.Text, index=False, unique=False)
    img = db.Column(db.String(256), index=False, unique=False)
    options = db.Column(db.Text, index=False, unique=False)

    def __repr__(self):
        return f'<Item {self.item}>'