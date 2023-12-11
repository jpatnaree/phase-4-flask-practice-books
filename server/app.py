#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Book, Publisher, Author # import your models here!

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

# write your routes here!

@app.get('/authors')
def get_authors():
    author = Author.query.all()
    
    data = [a.to_dict() for a in author]
    return make_response(jsonify(data), 200)

@app.get('/authors/<int:id>')
def get_author_by_id(id):
    author = db.session.get(Author, id)
    if not author:
        return make_response(jsonify({'error': 'Shumting Wong! no author'}), 404)
    
    return make_response(jsonify(author.to_dict(rules=('-publishers'))), 200)

@app.delete('/authors/<int:id>')
def delete_author(id):
    author = db.session.get(Author, id)
    if not author:
        return make_response(jsonify({'error': 'Shumting Wong! no author'}), 404)
    
    db.session.delete(author)
    db.session.commit()
    return make_response(jsonify({}), 204)

@app.get('/books')
def get_books():
    books = Book.query.all()
    
    book_dict = books.to_dict(rules=('-publishers', '-authors'))
    return make_response(jsonify(book_dict), 200)

@app.post('/books')
def post_book():
    data = request.json
    
    try:
        book = Book(
            name = data.get('name'),
            page_count = data.get('page_count'),
            author_name = data.get('author_name'),
            publisher_name = data.get('publisher_name')
        )
        db.session.add(book)
        db.session.commit()
        return make_response(jsonify(book.to_dict(rules=('-publishers', '-authors'))), 201)
    except:
        return make_response(jsonify({'error': 'Shumting Wong'}), 400)

@app.get('/publishers')
def get_publishers():
    pub = Publisher.query.all()
    
    return make_response(jsonify(p.to_dict() for p in pub), 200)

@app.get('/publishers/<int:id>')
def get_publisher_by_id(id):
    pub = db.session.get(Publisher, id)
    
    if not pub:
        return make_response(jsonify({'error': 'no publisher'}), 404)
    
    return make_response(jsonify(pub.to_dict(rules=('-books'))), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
