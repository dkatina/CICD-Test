from typing import List
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from sqlalchemy import Column, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)
ma = Marshmallow()

db.init_app(app) #Adding sqlalchemy extension to Flask
ma.init_app(app)

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

#========== Schemas ==========

#Validation, ensuring that incoming data satisfies what is required to create an instance for the desired
#Deserialization (converting incoming JSON into python)
#Serialization (Converting Model Objects into JSON)

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member

class LoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Loan

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)


#========= ROUTES ===========

#CREATE Member
@app.route("/members", methods=['POST'])
def create_member():
    #Validate and Deserialize incoming data
    try:
        member_data = member_schema.load(request.json)
    #If data invalid respond with error message
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #If data is valid, create new member with that data
    new_member = Member(name=member_data['name'], email=member_data['email'], phone=member_data['phone'])
    db.session.add(new_member) #Add to session
    db.session.commit() #commit session to db

    return member_schema.jsonify(new_member), 201 #return new_member object as a response

#RETRIEVE USERS
@app.route("/members", methods=["GET"])
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()

    return members_schema.jsonify(members), 200

#RETIEVE SPECIFIC USER localhost/members/1
@app.route("/members/<int:member_id>", methods=['GET'])
def get_member(member_id):
    member = db.session.get(Member, member_id)

    return member_schema.jsonify(member), 200

#UPDATE MEMBER
@app.route("/members/<int:member_id>", methods=['PUT'])
def update_member(member_id):
    member = db.session.get(Member, member_id)

    if member == None:
        return jsonify({"message": "invalid id"}), 400
    
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in member_data.items():
        if value:
            setattr(member, field, value)

    db.session.commit()
    return member_schema.jsonify(member), 200

#DELETE MEMBER
@app.route("/members/<int:member_id>", methods=['DELETE'])
def delete_member(member_id):
    member = db.session.get(Member, member_id)

    if member == None:
        return jsonify({"message": "invalid id"}), 400

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f"succeffuly deleted user {member_id}!"})



if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        
        

    app.run(debug=True)


    