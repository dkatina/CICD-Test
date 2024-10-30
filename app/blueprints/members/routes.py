from flask import request, jsonify
from app.blueprints.members import members_bp
from .schemas import member_schema, members_schema, login_schema
from marshmallow import ValidationError
from app.models import Member, db
from sqlalchemy import select
from app.extensions import limiter
from app.utils.util import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash

#Login Member
@members_bp.route("/login", methods=['POST'])
def login():
    #Validate the payload and ensure they sent us email and password
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Member).where(Member.email == creds['email'])
    member = db.session.execute(query).scalars().first()

    if member and check_password_hash(member.password, creds['password']): #If we have a member associated with the email, and the password is the same

        token = encode_token(member.id, member.role)

        response = {
            "message": "successfully logged in",
            "status": "success",
            "token": token
        }
    
    return jsonify(response), 200


#CREATE Member
@members_bp.route("/", methods=['POST'])
# @limiter.limit("3 per hour")
def create_member():
    #Validate and Deserialize incoming data
    try:
        member_data = member_schema.load(request.json)
    #If data invalid respond with error message
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #If data is valid, create new member with that data
    pwhash = generate_password_hash(member_data['password'])
    new_member = Member(name=member_data['name'], email=member_data['email'], phone=member_data['phone'], password=pwhash, role=member_data['role'])
    db.session.add(new_member) #Add to session
    db.session.commit() #commit session to db

    return member_schema.jsonify(new_member), 201 #return new_member object as a response

#RETRIEVE USERS
@members_bp.route("/", methods=["GET"])
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()

    return members_schema.jsonify(members), 200

#RETIEVE SPECIFIC USER localhost//1
@members_bp.route("/<int:member_id>", methods=['GET'])
def get_member(member_id):
    member = db.session.get(Member, member_id)

    return member_schema.jsonify(member), 200

#UPDATE MEMBER
@members_bp.route("/", methods=['PUT'])
@token_required
def update_member(token_user):
    member = db.session.get(Member, token_user)

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
@members_bp.route("/", methods=['DELETE'])
# @limiter.limit("3 per hour")
@token_required
def delete_member(token_user):
    
    
    member = db.session.get(Member, token_user)

    if member == None:
        return jsonify({"message": "invalid id"}), 400

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f"succeffuly deleted user {token_user}!"})