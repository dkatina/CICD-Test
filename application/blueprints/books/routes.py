from flask import request, jsonify
from application.blueprints.books import books_bp
from application.utils.util import admin_required
from .schemas import book_schema, books_schema
from marshmallow import ValidationError
from application.models import Book, db
from sqlalchemy import select
from application.extensions import limiter, cache

#CREATE book
@books_bp.route("/", methods=['POST'])
@admin_required
def create_book():
    #Validate and Deserialize incoming data
    try:
        book_data = book_schema.load(request.json)
    #If data invalid respond with error message
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #If data is valid, create new book with that data
    new_book = Book(title=book_data['title'], author=book_data['author'], genre=book_data['genre'], desc=book_data['desc'])
    db.session.add(new_book) #Add to session
    db.session.commit() #commit session to db

    return book_schema.jsonify(new_book), 201 #return new_book object as a response

#RETRIEVE book
@books_bp.route("/", methods=["GET"])
@limiter.limit("1000 per hour")
def get_books():
    print("GETTING BOOKS")
    page = request.args.get("page")
    page_size = request.args.get("page_size")
    print(page, page_size)
    query = select(Book)
    if page and page_size:
        books = db.paginate(query, page=int(page), per_page=int(page_size))
    else:
        books = db.session.execute(query).scalars().all()

    return books_schema.jsonify(books), 200

#RETIEVE SPECIFIC book localhost//1
@books_bp.route("/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = db.session.get(Book, book_id)

    return book_schema.jsonify(book), 200

#UPDATE book
@books_bp.route("/<int:book_id>", methods=['PUT'])
@admin_required
def update_book(book_id):
    book = db.session.get(Book, book_id)

    if book == None:
        return jsonify({"message": "invalid id"}), 400
    
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in book_data.items():
        if value:
            setattr(book, field, value)

    db.session.commit()
    return book_schema.jsonify(book), 200

#DELETE book
@books_bp.route("/<int:book_id>", methods=['DELETE'])
@admin_required
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if book == None:
        return jsonify({"message": "invalid id"}), 400

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"succeffuly deleted book {book_id}!"})

#Returns the most popular books
@books_bp.route("/popular", methods=["GET"])
def popular_books():
    query = select(Book)
    books = db.session.execute(query).scalars().all()

    #sort based on popularity
    books.sort(key=lambda book: len(book.loans), reverse=True)

    return books_schema.jsonify(books[:10]), 200

#Search Book using title as a search term
@books_bp.route("/search", methods=['GET'])
def search_book():
    
    title = request.args.get("title")
    if title:
        query = select(Book).where(Book.title.like(f"%{title}%"))
    else:
        query = select(Book)

    books = db.session.execute(query).scalars().all()

    return books_schema.jsonify(books), 200