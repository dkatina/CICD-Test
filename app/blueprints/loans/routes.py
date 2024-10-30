from flask import jsonify, request
from marshmallow import ValidationError
from app.blueprints.loans import loans_bp
from app.models import Loan
from app.utils.util import token_required
from .schemas import loan_schema, loans_schema, input_loan_schema
from datetime import date, datetime, timedelta
from app.models import db
from sqlalchemy import select

#create loan
@loans_bp.route("/", methods=['POST'])
@token_required
def create_loan(token_user):
    try:
        loan_data = input_loan_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
 
    if token_user != loan_data['member_id']:
        return jsonify({"message": "Invalid User Id"})

    new_loan = Loan(loan_date=datetime.now(), due_date= datetime.now() + timedelta(days=7), member_id=loan_data['member_id'])
    db.session.add(new_loan)
    db.session.commit()

    return loan_schema.jsonify(new_loan), 201

#get all loans
@loans_bp.route("/", methods=['GET'])
def get_loans():
    query = select(Loan)
    loans = db.session.execute(query).scalars().all()

    return loans_schema.jsonify(loans), 200
