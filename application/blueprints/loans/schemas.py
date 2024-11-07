from application.blueprints.books.schemas import BookSchema
from application.extensions import ma
from application.models import Loan
from marshmallow import fields

# class LoanSchema(ma.Schema):
#     id = fields.Integer(required=False)
#     member_id = fields.Integer(required=True)
#     loan_date = fields.Date(required=True)
#     due_date = fields.Date(required=True)

#     class Meta:
#         fields = ("member_id", "loan_date", "due_date", 'id')

class LoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Loan
        include_fk = True
    book_ids = fields.List(fields.Integer)
    books = fields.Nested("BookSchema", many=True )

loan_schema = LoanSchema()
input_loan_schema = LoanSchema(exclude=["loan_date", "due_date"])
loans_schema = LoanSchema(many=True)