from app.models import Member
from app.extensions import ma
from marshmallow import fields



class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
    loans = fields.Nested("LoanSchema", many=True)

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
login_schema = MemberSchema(exclude=['phone', 'name', 'role'])
update_schema = MemberSchema(exclude=['role'])