from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(1000), unique=True, nullable=False)
    url_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    source = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text)
    publication_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(1000))
    category = db.Column(db.String(50), nullable=False, default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    @staticmethod
    def generate_url_hash(url):
        return hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'summary': self.summary,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'image_url': self.image_url,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
