from  flask_sqlalchemy import SQLAlchemy
from  datetime import datetime
import random
import string


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(200), nullable=False)
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'User>>> {self.username}'

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=True)
    url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def generate_short_characters(self):
        picked_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        links = self.query.filter_by(short_url=picked_chars).first()
        if links:
            return self.generate_short_characters()
        return picked_chars


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return 'Bookmark>>> {self.url}'