from flask import Flask, render_template, request, redirect, url_for, helpers
from flask_restful import Api, Resource
from flask.helpers import make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BookDatabase import Base, Book
from flask_ngrok import run_with_ngrok
from flasgger import Swagger

libsearch = Flask(__name__)
searchlib = Api(libsearch)

engine = create_engine('sqlite:///books-collection.db', echo=True, connect_args={"check_same_thread": False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
swagger = Swagger(libsearch)
run_with_ngrok(libsearch)

class Books(Resource):
    def get(self):
        books = session.query(Book).all()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("books.html", books=books), 200, headers)

class addBooks(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("newBook.html"), 200, headers)

    def post(self):
        newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('books'))

class editBook(Resource):
    def get(self, book_id):
        editedBook = session.query(Book).filter_by(id=book_id).one()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("editBook.html", book=editedBook), 200, headers)

    def post(self, book_id):
        editedBook = session.query(Book).filter_by(id=book_id).one()
        if request.method == 'POST' or request.method == 'PUT':
            if request.form['name']:
                editedBook.title = request.form['name']
            if request.form['author']:
                editedBook.author = request.form['author']
            if request.form['genre']:
                editedBook.genre = request.form['genre']
                session.commit()
                return redirect(url_for('books'))

    def put(self, book_id):
        editedBook = session.query(Book).filter_by(id=book_id).one()
        if request.method == 'POST' or request.method == 'PUT':
            if request.form['name']:
                editedBook.title = request.form['name']
            if request.form['author']:
                editedBook.author = request.form['author']
            if request.form['genre']:
                editedBook.genre = request.form['genre']
                session.commit()
                return redirect(url_for('books'))


class deleteBook(Resource):
    def get(self, book_id):
        editedBook = session.query(Book).filter_by(id=book_id).one()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("deleteBook.html", book=editedBook), 200, headers)

    def post(self, book_id):
        bookToDelete = session.query(Book).filter_by(id=book_id).one()
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('books'))

    def delete(self, book_id):
        bookToDelete = session.query(Book).filter_by(id=book_id).one()
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('books'))


searchlib.add_resource(Books, '/', '/books/')
searchlib.add_resource(addBooks, '/books/new/')
searchlib.add_resource(editBook, '/books/<book_id>/edit/')
searchlib.add_resource(deleteBook, '/books/<book_id>/delete/')

if __name__ == '__main__':
    libsearch.debug = True
    libsearch.run()