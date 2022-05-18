from app import db
from datetime import datetime as dt, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, index=True, unique=True)
    token_exp = db.Column(db.DateTime)
    books = db.relationship('Book',
                    cascade = "all, delete",
                    backref = "user",
                    lazy = "dynamic"
                    )

    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_hashed_password(self, password):
        return check_password_hash(self.password, password)


    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def to_dict(self):
        return{
            'id': self.id,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "email": self.email,
            'created_on': self.created_on,
            'is_admin': self.is_admin,
            'token': self.token
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_book(self, book):
        self.books.append(book)
        db.session.commit()

    def remove_book(self, book):
        self.books.remove(book)
        db.session.commit()

    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        # give the user their back token if their is still valid
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        # if the token DNE or is exp
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=61)
    
    @staticmethod
    def check_token(token):
        u  = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    pages = db.Column(db.Integer)
    summary = db.Column(db.Text)
    image = db.Column(db.String)
    subject = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    user_id = db.Column(db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Book: {self.id} | {self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return{
            "title":self.title,
            "author":self.author,
            "pages": self.pages,
            "summary": self.summary,
            "image":self.image,
            "subject":self.subject,
            "created_on":self.created_on,
            "user_id":self.user_id
        }

    def from_dict(self, data):
        for field in ['title','author','pages','summary','image','subject','user_id']:
            if field in data:
                # object, attribute, value
                setattr(self, field, data[field])

