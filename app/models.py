from sqlalchemy.orm import relationship

from app.data_base import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique=True, index = True, nullable=False)
    email = Column(String, unique=True, index = True, nullable=False)
    password = Column(String, nullable=False)

    reviews = relationship('Review', back_populates = 'user')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, unique=True, index = True,nullable=False)
    author = Column(String, index = True, nullable=False)
    image_url = Column(String, index = True, nullable=True)
    description = Column(Text, index = True, nullable=True)

    reviews = relationship('Review', back_populates='book')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=True, index = True)
    rating = Column(Integer, nullable=False, index = True)

    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

    user = relationship('User', back_populates='reviews')
    book = relationship('Book', back_populates='reviews')