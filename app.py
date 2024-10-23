from typing import List
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)

db.init_app(app) #Adding sqlalchemy extension to Flask


#========== Models ==========

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



with app.app_context():
    # new_user = Member(name='Paul', email='paul@email', phone='123')
    # db.session.add(new_user)
    # db.session.commit()

    #READING DATA
    # query = select(Member).where(Member.name == 'Dylan')
    # dylan = db.session.execute(query).scalars().first()

    # print(dylan.email)


    #UPDATE DATA
    # dylan2 = db.session.get(Member, 1) #you can only do this for Primary keys

    # print(dylan2.name)
    # dylan2.name = 'DYLAN KATINA'
    # db.session.commit()
    # print(dylan2.name)

    #DELETE DATA
    # query = select(Member).where(Member.email == 'jilldoe@email.com')
    # jill = db.session.execute(query).scalars().first()

    # print(jill.name)
    # db.session.delete(jill)
    # db.session.commit()

    # new_loan = Loan(loan_date=date.today(), due_date=date.today(), member_id=1)
    # db.session.add(new_loan)
    # db.session.commit()

    #ADDING TO MANY-TO-MANY RELATIONSHIPS
    # book1 = db.session.get(Book, 3)
    # book2 = db.session.get(Book, 2)
    # book3 = db.session.get(Book, 1)

    # loan = db.session.get(Loan, 1)
    # loan.books.append(book1)
    # loan.books.append(book2)
    # loan.books.append(book3)
    
    # db.session.commit()

    # dylan = db.session.get(Member,1)

    # for loan in dylan.loans:
    #     print("Loan ID:", loan.id)
    #     for book in loan.books:
    #         print(book.title)
    # user = db.session.get(Member, 1)
    # print(user.name)
    pass

    



    
   


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        
        

    app.run()


    