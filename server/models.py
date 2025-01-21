from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validator for name (cannot be empty string)
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Name cannot be empty.')

        # Check for uniqueness manually
        existing_author = db.session.query(Author).filter_by(name=value).first()
        if existing_author:
            raise ValueError(f'An author with the name "{value}" already exists.')
        return value

    # Validator for phone_number (must be exactly 10 digits and only digits)
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value:
            if len(value) != 10 or not value.isdigit():
                raise ValueError('Phone number must be exactly 10 digits and contain only numbers.')
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validator for content (at least 250 characters)
    @validates('content')
    def validates_content(self, key, value):
        if value and len(value) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return value

    # Validator for summary (max 250 characters)
    @validates('summary')
    def validates_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError('Summary must be maximum 250 characters long.')
        return value

    # Validator for category (must be Fiction or Non-Fiction)
    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either "Fiction" or "Non-Fiction".')
        return value

    # Validator for title (must contain clickbait keywords)
    @validates('title')
    def validate_title(self, key, value):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError('Title must contain one of the following clickbait phrases: "Won\'t Believe", "Secret", "Top", "Guess".')
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'