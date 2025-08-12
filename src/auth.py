from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity
import datetime

from src.constants.http_status_code import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from src.database import User, db

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.route('/login', methods=['POST'])
def login():
    # Ensure JWT_SECRET_KEY is set
    if 'JWT_SECRET_KEY' not in current_app.config or not current_app.config['JWT_SECRET_KEY']:
        return jsonify({"error": "JWT_SECRET_KEY is not set in app config"}), HTTP_401_UNAUTHORIZED

    # Ensure JWT_REFRESH_TOKEN_EXPIRES is set as a timedelta inside the app context
    if 'JWT_REFRESH_TOKEN_EXPIRES' not in current_app.config or not isinstance(current_app.config['JWT_REFRESH_TOKEN_EXPIRES'], datetime.timedelta):
        current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)

    data = request.get_json()
    identifier = data.get('identifier')  # can be email or username
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"error": "Identifier and password are required"}), HTTP_400_BAD_REQUEST

    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    if user and check_password_hash(user.password, password):
        refresh_token = create_refresh_token(identity=str(user.id))
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user.username,
                "email": user.email,
                "access_token": access_token,
                "refresh_token": refresh_token
            },
        }), HTTP_200_OK
    else:
        return jsonify({"error": "Invalid credentials"}), HTTP_401_UNAUTHORIZED

@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not username or not password or not email:
        return jsonify({"error": "Username, password, and email are required"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), HTTP_400_BAD_REQUEST
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters long"}), HTTP_400_BAD_REQUEST
    if not username.isalnum():
        return jsonify({"error": "Username must be alphanumeric and cannot contain spaces"}), HTTP_400_BAD_REQUEST
    if not validators.email(email):
        return jsonify({"error": "Invalid email address"}), HTTP_400_BAD_REQUEST
    if User.query.filter(User.email == email).first():
        return jsonify({"error": "Email is taken"}), HTTP_409_CONFLICT
    if User.query.filter(User.username == username).first():
        return jsonify({"error": "Username is taken"}), HTTP_409_CONFLICT
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user": {
        "username": user.username,
        "email": user.email,
    }}), HTTP_201_CREATED

@auth.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful"}), HTTP_200_OK

@auth.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=int(user_id)).first()
    if not user:
        return jsonify({"error": "User not found"}), HTTP_401_UNAUTHORIZED
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return jsonify(user_data), HTTP_200_OK


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    return jsonify({"access_token": access_token}), HTTP_200_OK
