from flask import Flask, render_template, request, redirect, url_for

libsearch = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BookDatabase import Base, Book
from flask_ngrok import run_with_ngrok
from flasgger import Swagger


engine = create_engine('sqlite:///books-collection.db', echo=True, connect_args={"check_same_thread": False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
swagger = Swagger(libsearch)
run_with_ngrok(libsearch)


@libsearch.route('/')
@libsearch.route('/books', methods=['GET', 'POST'])
def showBooks():
    books = session.query(Book).all()
    return render_template("books.html", books=books)


@libsearch.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')


@libsearch.route("/books/<int:book_id>/edit/", methods=['GET', 'PUT'])
def editBook(book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'GET':
        if request.form['name']:
            editedBook.title = request.form['title']
            return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html', book=editedBook)


@libsearch.route('/books/<int:book_id>/delete/', methods=['GET', 'DELETE'])
def deleteBook(book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'GET':
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('showBooks', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)


if __name__ == '__main__':
    libsearch.debug = True
    libsearch.run()