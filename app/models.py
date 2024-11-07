from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column
from typing import List
from datetime import date


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)

loan_book = db.Table(
    "loan_book",
    Base.metadata,
    Column("loan_id", db.ForeignKey("loans.id")),
    Column("book_id", db.ForeignKey("books.id"))
)


class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20))
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    role: Mapped[str] = mapped_column(db.String(50), nullable=False)

    #One-to-Many
    loans: Mapped[List['Loan']] = db.relationship(back_populates='member')


class Loan(Base):
    __tablename__ = 'loans'

    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(nullable=False)
    due_date: Mapped[date] = mapped_column(nullable=False)
    member_id: Mapped[int] = mapped_column(db.ForeignKey('members.id'))

    #Many-to-One
    member: Mapped['Member'] = db.relationship(back_populates='loans')
    #Many-to-Many
    books: Mapped[List['Book']] = db.relationship(secondary=loan_book, back_populates='loans')

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    author: Mapped[str] = mapped_column(db.String(100), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(50), nullable=False)
    desc: Mapped[str] = mapped_column(db.String(300), nullable=False)

    loans: Mapped[List['Loan']] = db.relationship(secondary=loan_book, back_populates='books')