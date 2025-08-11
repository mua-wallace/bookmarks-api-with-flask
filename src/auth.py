from  flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from src.constants.http_status_code import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # For demonstration purposes, we will just check if the username and password are not empty
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # In a real application, you would verify the credentials against a database
    if username == 'admin' and password == 'password':
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), HTTP_400_BAD_REQUEST
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters long"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or '' in username:
        return jsonify({"error": "Username must be alphanumeric and cannot contain spaces"}), HTTP_400_BAD_REQUEST

@auth.route('/logout', methods=['POST'])
def logout():
    # For demonstration purposes, we will just return a success message
    return jsonify({"message": "Logout successful"}), 200

@auth.route('/me', methods=['GET'])
def me():
    # For demonstration purposes, we will just return a dummy user
    user = {
        "id": 1,
        "username": "admin",
        "email": "admin@gmail.com",
        "role": "admin"
    }

    return jsonify(user), 200
