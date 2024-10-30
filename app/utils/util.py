from flask import request, jsonify
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
import os

SECRET_KEY = os.environ.get('SECRET_KEY') #Secret kept secret in my .env, used to mint my tokens

#creates a token using a members id
def encode_token(member_id, role):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days = 0, hours= 1), #adding expriation to toklen 1 hour after now
        'iat': datetime.now(timezone.utc), #Issued at iat
        'sub': member_id, #Sub == subject of the token
        'role': role
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


#token reuiqred decorated
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs): #Taking in args and kwargs needed for the decorated function
        token = None

        if 'Authorization' in request.headers:
            try: 
                token = request.headers['Authorization'].split()[1]

                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("PAYLOAD:", payload)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid Token"}), 401
            return func(token_user=payload['sub'],*args, **kwargs) #executing the function that is being decorated
        else:
            return jsonify({"messages": "Token Authorization Required"}), 401
        
    return wrapper


#admin_required wrapper
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs): #Taking in args and kwargs needed for the decorated function
        token = None

        if 'Authorization' in request.headers:
            try: 
                token = request.headers['Authorization'].split()[1]

                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("PAYLOAD:", payload)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid Token"}), 401
            
            if payload['role'] == 'admin':
                return func(*args, **kwargs) #executing the function that is being decorated
            else:
                return jsonify({"messages": "Admin Authorization Required"}), 401
        else:
            return jsonify({"messages": "Token Authorization Required"}), 401
        
    return wrapper

