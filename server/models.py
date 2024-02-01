from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        author = db.session.query(Author.id).filter_by(name = name).first()
        if not name:
            raise ValueError("Name field is required.")
        if author is not None:
            raise ValueError("Name must be unique.")
        else:
            return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be 10 digits")

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title")
        
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title
        
        
    @validates('content', 'summary')
    def validate_length(self, key, string):
        if (key == "content"):
            if len(string) < 250:
                raise ValueError("Content must have at least 250 characters.")
        elif (key == "summary"):
            if len(string) > 250:
                raise ValueError("Summary cannot have more than 250 characters.")
        else:
            return string
        
    @validates('category')
    def validate_category(self, key, category):
        if category == "Fiction" or category == "Non-Fiction":
            return category
        else:
            raise ValueError("This category is not recognized.")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
