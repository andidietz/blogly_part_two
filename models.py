from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default='https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png')

    posts = db.relationship('Post', backref='user')

    def __repr__(self):
        p = self
        return f'<User {p.id} {p.first_name} {p.last_name}>'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    __tablename__= 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))