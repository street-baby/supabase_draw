from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    images = db.relationship('GeneratedImage', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None
        }

class GeneratedImage(db.Model):
    __tablename__ = 'generated_images'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    style = db.Column(db.String(50))
    ratio = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'prompt': self.prompt,
            'image_url': self.image_url,
            'style': self.style,
            'ratio': self.ratio,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }