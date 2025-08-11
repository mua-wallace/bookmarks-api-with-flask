from flask import Blueprint, render_template
import requests

bookmarks = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')
@bookmarks.route('/', methods=['GET'])
def get_bookmarks():
    # For demonstration purposes, we will return a static list of bookmarks
    bookmarks_list = [
        {"id": 1, "title": "Flask Documentation", "url": "https://flask.palletsprojects.com/"},
        {"id": 2, "title": "Python Official Website", "url": "https://www.python.org/"},
        ]
    return {"bookmarks": bookmarks_list}, 200

@bookmarks.route('/<int:bookmark_id>', methods=['GET'])
def get_bookmark(bookmark_id):
    # For demonstration purposes, we will return a static bookmark
    bookmark = {"id": bookmark_id, "title": "Flask Documentation", "url": "https://flask.palletsprojects.com/"}
    return {"bookmark": bookmark}, 200

@bookmarks.route('/add', methods=['POST'])
def add_bookmark():
    # For demonstration purposes, we will just return a success message
    return {"message": "Bookmark added successfully"}, 201

@bookmarks.route('/<int:bookmark_id>/edit', methods=['PUT'])
def edit_bookmark(bookmark_id):
    # For demonstration purposes, we will just return a success message
    return {"message": f"Bookmark {bookmark_id} edited successfully"}, 200

@bookmarks.route('/<int:bookmark_id>/delete', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    # For demonstration purposes, we will just return a success message
    return {"message": f"Bookmark {bookmark_id} deleted successfully"}, 200
@bookmarks.route('/search', methods=['GET'])
def search_bookmarks():
    query = requests.args.get('query', '')
    # For demonstration purposes, we will return a static list of bookmarks that match the query
    bookmarks_list = [
        {"id": 1, "title": "Flask Documentation", "url": "https://flask.palletsprojects.com/"},
        {"id": 2, "title": "Python Official Website", "url": "https://www.python.org/"},
    ]
    filtered_bookmarks = [b for b in bookmarks_list if query.lower() in b['title'].lower()]
    return {"bookmarks": filtered_bookmarks}, 200