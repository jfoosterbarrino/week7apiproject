from . import bp as api
from app.models import *
from flask import make_response, request, abort, g
from app.blueprints.auth.authy import token_auth
from helpers import require_admin
from flask_login import current_user

@api.get('/user')
def get_all_users():
    users = User.query.all()
    users = [user.to_dict() for user in users]
    return make_response({"users": users},200)

@api.post('/user')
def post_user():
    post_data = request.get_json()
    user = User(**post_data)
    user.save()
    return make_response(f'User Id: {user.id} has been created', 200)

@api.put('/user/<int:id>')
@token_auth.login_required()
@require_admin
def put_user(id):
    put_data = request.get_json()
    user = User.query.get(id)
    if not user:
        abort(404)
    user.from_dict(put_data)
    user.save()
    return make_response(f'User Id: {user.id} has been changed', 200)

@api.delete('/user/<int:id>')
@token_auth.login_required
@require_admin
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    user.delete()
    return make_response(f'User Id: {id} has been deleted', 200)

@api.get('/book')
def get_all_books():
    books = Book.query.all()
    books = [book.to_dict() for book in books]
    return make_response({"books":books},200)

@api.get('/book/<int:id>')
def get_book(id):
    book = Book.query.get(id)
    if not book:
        abort(404)
    return make_response(book.to_dict(), 200)

@api.post('/book')
@token_auth.login_required
@require_admin
def post_book():
    post_data = request.get_json()
    book = Book(**post_data)
    book.save()
    user = User.query.get(book.user_id)
    user.books.append(book)
    user.save()
    return make_response(f'Book Id: {book.id} has been created', 200)

@api.put('/book/<int:id>')
@token_auth.login_required
@require_admin
def put_book(id):
    put_data = request.get_json()
    book = Book.query.get(id)
    if not book:
        abort(404)
    book.from_dict(put_data)
    book.save()
    return make_response(f'Book Id: {book.id} has been changed', 200)

@api.delete('/book/<int:id>')
@token_auth.login_required
@require_admin
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        abort(404)
    book.delete()
    return make_response(f'Book Id: {id} has been deleted', 200)
