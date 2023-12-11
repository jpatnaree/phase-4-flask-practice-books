from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# write your models here!
class Book(db.Model, SerializerMixin):
    __tablename__ = 'book_table'
    
    serialize_rules = ('-publishers.books',)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    page_count = db.Column(db.Integer, nullable=False)
    
    author_name = db.Column(db.String, db.ForeignKey('author_table.title'), nullable=False)
    publisher_name = db.Column(db.String, db.ForeignKey('publisher_table.title'), nullable=False)
    
    publishers = db.relationship('Publisher', back_populates='books', cascade='all, delete-orphan')
    authors = association_proxy('publishers', 'authors')
    
    @validates('page_count')
    def validate_page_count(self, key: int, value: int):
        if value <= 0:
            raise ValueError('at least one page pleaseee')
        return value
    
class Publisher(db.Model, SerializerMixin):
    __tablename__ = 'publisher_table'
    
    serialize_rules = ('-authors.publishers', '-books.publishers')
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    founding_year = db.Column(db.Integer, nullable=False)
    
    authors = db.relationship('Author', back_populates='publishers')
    books = db.relationship('Book', back_populates='publishers')
    
    @validates('founding_year')
    def validate_founding_year(self, key: int, value: int):
        
        current_year = datetime.now().year
        if 1600 <= value <= current_year:
            return value
        
        raise ValueError('Wrong year!')
    
class Author(db.Model, SerializerMixin):
    __tablename__ = 'author_table'
    
    serialize_rules = ('-publishers.author',)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    pen_name = db.Column(db.String)
    
    publishers = db.relationship('Publisher', back_populates='authors', cascade='all, delete-orphan')
    books = association_proxy('publishers', 'books')