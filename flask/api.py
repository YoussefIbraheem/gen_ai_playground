from app import app , db
from models import Book , Author , Review
from flask import Flask , jsonify

def list_book_to_dict(book):
    return {'id': book.id, 'title': book.title, 'author': book.author.name}
    

@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([list_book_to_dict(book) for book in books])

@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.filter_by(id=id).first_or_404()
    return jsonify(list_book_to_dict(book))

@app.route('/api/books', methods=['POST'])
def create_book():
    title = request.json['title']
    author_name = request.json['author']
    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()
    if title:
        book = Book(title=title, author_id=author.id)
        db.session.add(book)
        db.session.commit()
    return jsonify(list_book_to_dict(book))

@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.filter_by(id=id).first_or_404()
    title = request.json['title']
    author_name = request.json['author']
    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()
    if title:
        book.title = title
        book.author_id = author.id
        db.session.commit()
    return jsonify(list_book_to_dict(book))

@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(id=id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})