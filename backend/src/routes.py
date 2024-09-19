from flask import request, jsonify, Blueprint
from src.db import Blog
from src.db import User
from src.db import db


# USER ROUTES:
user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    return jsonify([user.to_dict() for user in all_users])


@user_routes.route("/users/<string:username>", methods=["GET"])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200


@user_routes.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


@user_routes.route("/users/<string:username>", methods=["DELETE"])
def delete_user_by_name(username):
    # get user with username
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"})
    # first delete all the user's blogs
    for blog in user.blogs:
        db.session.delete(blog)
    # finally delete the user
    db.session.delete(user)
    db.session.commit()
    return "", 204


# BLOG ROUTES:
blog_routes = Blueprint("blog_routes", __name__)


@blog_routes.route("/blogs", methods=["GET"])
def get_blogs():
    all_blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in all_blogs])


@blog_routes.route("/blogs", methods=["POST"])
def add_blog():
    data = request.json
    # check the associated author exists
    author = User.query.get_or_404(data["author_id"])
    # add new blog
    new_blog = Blog(title=data["title"], author_id=author.id, content=data["content"])
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(new_blog.to_dict()), 201


@blog_routes.route("/blogs/<int:blog_id>", methods=["PUT"])
def update_blog(blog_id):
    # check the blog to update exists
    blog = Blog.query.get_or_404(blog_id)
    data = request.json
    # check the user id to be put into this resource exists
    new_author = User.query.get_or_404(data["author_id"])
    # update blog
    blog.title = data["title"]
    blog.author_id = new_author.id
    blog.content = data["content"]
    db.session.commit()
    return jsonify(blog.to_dict())


@blog_routes.route("/blogs/<int:blog_id>", methods=["DELETE"])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return "", 204
