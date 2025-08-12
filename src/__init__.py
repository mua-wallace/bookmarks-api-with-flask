from flask import Flask
from src.auth import auth
from src.bookmarks import bookmarks
import os
from src.database import db
from  flask_jwt_extended import JWTManager
from datetime import timedelta


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the default configuration
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES= timedelta(hours=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', '1'))),
            JWT_REFRESH_TOKEN_EXPIRES= timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', '30'))),
        )
    else:
        # Load the test configuration if provided
        app.config.from_mapping(test_config)

    # Initialize the database
    db.app = app
    db.init_app(app)
    # Initialize JWT Manager
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    return app