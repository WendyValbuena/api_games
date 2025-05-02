from flask import Blueprint, jsonify, request
import jwt
import datetime
from functools import wraps
import json

with open('conf.json', 'r') as f:
    config = json.load(f)
SECRET_KEY = config.get('SECRET_KEY')

login_bp = Blueprint('login', __name__)

users = [
    {'username': 'user_01', 'password': '12345qwertz', 'role': 'admin'},
    {'username': 'user_02', 'password': '7890qwertz', 'role': 'user'}
]

#token required
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated_function

# Login
@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # valid credentials
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # token / hours
    token = jwt.encode({
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})

# Protected
@login_bp.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Hello {current_user}, you are authorized!'})
