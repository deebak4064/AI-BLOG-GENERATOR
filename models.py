"""Database models for user authentication."""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_password(self, password):
        """Hash and set the user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class UserBlog(db.Model):
    """Per-user saved/generated blog entries."""
    __tablename__ = 'user_blogs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(256), nullable=False)
    details = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    body_html = db.Column(db.Text, nullable=True)
    filename_base = db.Column(db.String(160), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)

    user = db.relationship('User', backref=db.backref('blogs', lazy='dynamic'))

    def to_dict(self):
        fb = self.filename_base
        if not fb and self.title:
            fb = ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in self.title.lower())[:120]
        return {
            'id': self.id,
            'title': self.title,
            'details': self.details,
            'body': self.body,
            'body_html': self.body_html,
            'filename_base': fb,
            'date': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
