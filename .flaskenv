
export FLASK_ENV=development
export FLASK_APP=src

export SQLALCHEMY_DATABASE_URI=sqlite:///bookmark.db
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export JWT_SECRET_KEY=supersecretkey
export JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour
export JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days